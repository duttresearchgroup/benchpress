import logging
import time
from jaeger_client import Config
import opentracing

import subprocess
import sys
import os

dashboard_id = "hInD3dM7z"

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
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

def main():
    tracer = init_tracer('Benchpress')
    span = tracer.start_span(operation_name="fio")
    
    span.set_tag('Application', sys.argv[1])
    span.set_tag('Test', sys.argv[2])
    for n in range(3, len(sys.argv), 2):
        span.set_tag(sys.argv[n], sys.argv[n+1])
    span.set_tag('Freq', "auto")

    result = subprocess.run(
        [
            "/usr/local/bin/docker-compose", 
            "-f", 
            os.path.dirname(os.path.realpath(__file__))+"/../docker-compose.yml",
            "run", 
            "benchpress", 
            "python3", 
            "benchpress_cli.py", 
            "-b", 
            "benchmarks.yml", 
            "-j", 
            "jobs/jobs.yml", 
            "run", 
            "{0} {1}".format(sys.argv[1], sys.argv[2])
        ])

    span.finish()

    # with tracer.start_span('TestSpan') as span:
    #     span.log_kv({'event': 'test message', 'life': 42})

    #     with tracer.start_span('ChildSpan', child_of=span) as child_span:
    #         child_span.log_kv({'event': 'down below'})

    
    time.sleep(2)   # yield to IOLoop to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50

    logging.info("Jaeger URL: http://deep.ics.uci.edu:16686/trace/" + format(span.trace_id, 'x'))
    logging.info("Grafana URL: http://deep.ics.uci.edu:3000/d/{0}/node-exporter-full?from={1}&to={2}".format(dashboard_id, int(span.start_time*1000), int(span.end_time*1000)))

    tracer.close()  # flush any buffered spans

if __name__ == "__main__":
    if (len(sys.argv)<3):
        print ('Required params:', sys.argv[0], '<application> <test>')

    else:
        main()