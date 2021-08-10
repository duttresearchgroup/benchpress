import logging
import time
from jaeger_client import Config

import subprocess
import sys

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': 'deep.ics.uci.edu',
                'reporting_port': '6831',
            },
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

if __name__ == "__main__":
    tracer = init_tracer('Benchpress')

    result = subprocess.run(
        [
            "/usr/local/bin/docker-compose", 
            "run", 
            "benchpress", 
            "python3", 
            "benchpress_cli.py", 
            "-b", 
            "benchmarks.yml", 
            "-j", 
            "jobs/jobs.yml", 
            "run", 
            "fio aio"
        ])

    # with tracer.start_span('TestSpan') as span:
    #     span.log_kv({'event': 'test message', 'life': 42})

    #     with tracer.start_span('ChildSpan', child_of=span) as child_span:
    #         child_span.log_kv({'event': 'down below'})

        
    # time.sleep(2)   # yield to IOLoop to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50
    tracer.close()  # flush any buffered spans