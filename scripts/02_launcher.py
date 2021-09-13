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


def launch_container(app_test_str, scale):
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
        ])

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

    launch_container(app_test_str, scale)

    span.finish()

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
    args = parser.parse_args()

    if (args.app_name is None):
        parser.print_help()
    else:
        main(args)