// Copyright 2021 The Prometheus Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// +build linux
// +build !notplink

package collector

import (
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/go-kit/log"
	"github.com/prometheus/client_golang/prometheus"
)

type tplinkCollector struct {
	energyCore typedDesc
	logger     log.Logger
}

func init() {
	registerCollector("tplink", defaultEnabled, TpLinkCollector)
}

// TpLinkCollector returns a new Collector exposing load average stats.
func TpLinkCollector(logger log.Logger) (Collector, error) {
	return &tplinkCollector{
		energyCore: typedDesc{prometheus.NewDesc(
			prometheus.BuildFQName(namespace, "tplink", "energy"),
			"The AC energy reported by TP Link.",
			nil, nil,
		), prometheus.CounterValue},
		logger: logger,
	}, nil
}

func (c *tplinkCollector) Update(ch chan<- prometheus.Metric) error {
	var power []byte
	var err error
	var cmdOut *exec.Cmd
	var output string

	cmdOut = exec.Command("/bin/sh", "-c", "/usr/local/bin/kasa | /usr/bin/grep current")
	if power, err = cmdOut.Output(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	output = strings.Trim(string(power), "\n")
	// ch <- c.energyCore.mustNewConstMetric(string(output))
	ch <- c.energyCore.GetMetricWithLabelValues(output)
	return nil
}
