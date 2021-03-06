#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from .django_workload import DjangoWorkloadParser
from .fio import FioParser
from .gapbs import GAPBSParser
from .generic import JSONParser
from .graph500 import Graph500Parser
from .ltp import LtpParser
from .nginx_wrk_bench import NginxWrkParser
from .minebench import KMeansParser
from .minebench import PLSAParser
from .minebench import RSearchParser
from .returncode import ReturncodeParser
from .schbench import SchbenchParser
from .silo import SiloParser


def register_parsers(factory):
    factory.register('django_workload', DjangoWorkloadParser)
    factory.register('fio', FioParser)
    factory.register('gapbs', GAPBSParser)
    factory.register('graph500', Graph500Parser)
    factory.register('json', JSONParser)
    factory.register('ltp', LtpParser)
    factory.register('nginx_wrk_bench', NginxWrkParser)
    factory.register('minebench_kmeans', KMeansParser)
    factory.register('minebench_plsa', PLSAParser)
    factory.register('minebench_rsearch', RSearchParser)
    factory.register('returncode', ReturncodeParser)
    factory.register('schbench', SchbenchParser)
    factory.register('silo', SiloParser)
