import logging
import time
from jaeger_client import Config
import opentracing

import subprocess
import sys
import os
import argparse

dashboard_id = "hInD3dM7z"

parser = argparse.ArgumentParser(description='Launch benchpress applications with Jaeger.')

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': 'deep.ics.uci.edu',
                'reporting_port': '6831',
                # 14268 for tempo backend
            },
            'logging': False,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


def launch_container(app_test_str, scale,out_folder_,log_file_name_):
    f = open(os.path.dirname(os.path.realpath(__file__))+"/../fbkutils/benchpress/launch.sh", "w")
    f.write("python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run \""+app_test_str+"\"")
    f.close()

    result = subprocess.run(
        [
            "/usr/local/bin/docker-compose", 
            "-f", 
            os.path.dirname(os.path.realpath(__file__))+"/../docker-compose.yml",
            "up", 
            "--scale", 
            "benchpress={0}".format(scale)
        ],
        capture_output = True )
    f2 = open(os.path.dirname(os.path.realpath(__file__))+ "/"+out_folder_+"/"+log_file_name_+".log","w+")
    f2.write(result.stdout.decode("utf-8"))
    f2.close()

# extract the performance parameter from different application logs and return them
def log_parser(app,args_,log_file_name_,out_folder_):
    # file = open(os.path.dirname(os.path.realpath(__file__))+"/"+args_.out_folder+"/"+log_file_name_+".log","r")
    file = open(os.path.dirname(os.path.realpath(__file__))+ "/"+out_folder_+"/"+log_file_name_+".log","r")
    if app == "schbench":
        for line in file:
            if "p99_9" in line:
                # logging.info(line)
                ans =  line[line.find("p99_9")+7:line.find("}",line.find("p99_9"),-1)]
                return float(ans)
    if app == "nginx_wrk_bench":
        for line in file:
            if "Requests/sec" in line:
                # logging.info(line)
                ans = line[line.find("Requests/sec")+14:line.find("}",line.find("Requests/sec"),-1)]
                return float(ans)
    if app == "minebench_plsa":
        for line in file:
            if "total_time" in line:
                # logging.info(line)
                ans = line[line.find("total_time")+12:line.find("}",line.find("total_time"),-1)]
                return float(ans)
    if app == "gapbs_bc":
        for line in file:
            if "generate_time" in line:
                # logging.info(line)
                ans = line[line.find("generate_time")+15:line.find(",",line.find("generate_time"),-1)]
                return float(ans)
    if app == "fio":
        for line in file:
            if '"iops"'in line:
                # logging.info(line)
                ans = line[line.find('"iops"')+6:line.find(",",line.find('"iops"'),-1)]
                return float(ans)


def normalize_res(app_name,value):
    if app_name == "schbench":
        logging.info("schbench")
        res = (174000-value)/174000
        return res
    elif app_name == "nginx_wrk_bench":
        logging.info("nginx_wrk_bench")
        res = (14500-value)/14500
        return res
    elif app_name == "minebench_plsa":
        logging.info("minebench_plsa")
        res = (39-value)/39
        return res
    elif app_name == "gapbs_bc":
        logging.info("gapbs_bc")
        res = (0.99-value)/0.99
        return res
    elif app_name == "fio":
        logging.info("fio")
        res = (678-value)/678
        return res

def main(args):
    tracer = init_tracer('Benchpress')
    span = tracer.start_span(operation_name="Profile")
    
    span.set_tag('Application', args.app_name)
    app_test_str = ""
    try:
        if(args.test):
            app_test_str =  "{0} {1}".format(args.app_name, args.test)
            span.set_tag('Test', args.test)
        else:
            raise AttributeError
    except AttributeError:
        app_test_str =  "{0}".format(args.app_name)
        print ("No test name detected")
    
    try:
        args.turbo
        span.set_tag('Turbo Mode', args.turbo)
    except AttributeError:
        print ("Turbo Mode not specified")

    try:
        args.freq
        span.set_tag('Frequency', args.freq)
    except AttributeError:
        print ("Frequency not specified")

    scale=1
    try:
        if(args.scale):
            scale=args.scale
        else:
            raise AttributeError            
    except AttributeError:
        span.set_tag('Scale', scale)
        print ("Scale not specified, defaulting to 1")
    
    log_file_name = app_test_str.split()[0]+"_freq_"+str(args.freq)+"_scale_"+str(args.scale)+"_ite"+str(args.iter)
    path_name = os.path.dirname(os.path.realpath(__file__))
    # logging.info(app_name+"_freq_"+str(args.freq)+"_scale_"+str(args.scale)+"_ite")
    launch_container(app_test_str, scale,args.out_folder,log_file_name)
    
    span.finish()
    res=log_parser(app_test_str.split()[0],args,log_file_name,args.out_folder)
    nor_res = normalize_res(app_test_str.split()[0],res)
    logging.info(nor_res)
    span.set_tag('Performance',nor_res)

    time.sleep(2)   # yield to IOLoop to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50
    
    logging.info("Jaeger URL: http://deep.ics.uci.edu:16686/trace/" + format(span.trace_id, 'x'))
    logging.info("Grafana URL: http://deep.ics.uci.edu:3000/d/{0}/node-exporter-full?from={1}&to={2}".format(dashboard_id, int(span.start_time*1000), int(span.end_time*1000)))

    tracer.close()  # flush any buffered spans
    
if __name__ == "__main__":
    parser.add_argument('app_name', metavar='<APPLICATION>', type=str, help='application name')
    parser.add_argument('--test', metavar='<TEST>', type=str, help='Test name', nargs='?')
    parser.add_argument('--turbo', metavar='<1/0>', type=int, help='Turbo Mode status')
    parser.add_argument('--freq', metavar='<FREQUENCY>', type=int, help='Turbo Frequency', nargs='?')
    parser.add_argument('--scale', metavar='<SCALE>', type=int, help='Number of instances', nargs='?')
    parser.add_argument('--out_folder', metavar='<OUTFOLDER>', type=str, help='output folder name', nargs='?')
    parser.add_argument('--iter', metavar='<ITER>', type=int, help='iteration', nargs='?')
    args = parser.parse_args()

    if (args.app_name is None):
        parser.print_help()
    else:
        main(args)