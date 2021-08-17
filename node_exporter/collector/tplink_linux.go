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
	// "encoding/json"
	"fmt"
	"github.com/go-kit/log"
	"github.com/prometheus/client_golang/prometheus"
	"os/exec"
	"strconv"
	"strings"
)

type TPLinkPower struct {
	Current float64 `json:"current"`
	Voltage float64 `json:"voltage"`
	Power   float64 `json:"power"`
	Total   float64 `json:"total"`
	ErrCode int     `json:"err_code"`
}

type tplinkCollector struct {
	powerNode typedDesc
	logger    log.Logger
}

func init() {
	registerCollector("tplink", defaultEnabled, TpLinkCollector)
}

// TpLinkCollector returns a new Collector exposing load average stats.
func TpLinkCollector(logger log.Logger) (Collector, error) {
	return &tplinkCollector{
		powerNode: typedDesc{prometheus.NewDesc(
			prometheus.BuildFQName(namespace, "tplink", "power"),
			"The AC power reported by TP Link.",
			nil, nil,
		), prometheus.GaugeValue},
		logger: logger,
	}, nil
}

func (c *tplinkCollector) Update(ch chan<- prometheus.Metric) error {
	var execResult []byte
	var err1 error
	args := []string{"--host", "128.195.55.227", "--plug", "emeter"}
	if execResult, err1 = exec.Command("kasa", args...).Output(); err1 != nil {
		fmt.Print("TPlink Collector error: ", err1)
		return nil
	}

	execResultString := string(execResult)
	startPower := strings.Index(execResultString, "Power:") + 7
	endPower := strings.Index(execResultString, "Total") - 3
	powerString := execResultString[startPower:endPower]
	// ***************************************************
	// Extract from JSON
	// ***************************************************
	// powerString := execResultString[strings.LastIndex(execResultString, "{") : len(execResultString)-2]
	// powerString = strings.ReplaceAll(powerString, "'", "\"")
	// var power TPLinkPower
	// err1 = json.Unmarshal([]byte(powerString), &power)
	// if err1 != nil {
	// 	fmt.Printf("TPlink Parse error: %s\n", err1)
	// 	return nil
	// }
	// // fmt.Printf("Current: %f, Voltage: %f, Power: %f, Total: %f, Error: %d\n", power.Current, power.Voltage, power.Power, power.Total, power.ErrCode)
	// ***************************************************
	powerF, err1 := strconv.ParseFloat(powerString, 64)
	if err1 != nil {
		fmt.Print("TPlink parse float error: ", err1)
	} else {
		ch <- c.powerNode.mustNewConstMetric(powerF)
	}

	return nil
}
