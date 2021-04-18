#!/usr/bin/python
# coding=utf-8
"""
@author: qyke
获取sonar 项目数据
"""

import requests
import json
from auto_report.logger import Log


class SonarHandel:
    def __init__(self, sonar_url, sonar_token):
        """
        :param sonar_url: string sonar 地址
        :param sonar_token: string token
        """
        self.url = sonar_url.strip('/')
        self.token = sonar_token

    def get_component_data(self, sonar_component, sonar_metricKeys):
        """
        :param sonar_component: string 项目名称
        :param sonar_metricKeys: list 获取的字段名
        (https://docs.sonarqube.org/latest/user-guide/metric-definitions/)
        :return: list['字段名': value]
        """
        result = dict()
        metricKeys_string = ",".join(sonar_metricKeys)
        # 请求参数拼接
        component_url = self.url + "/api/measures/component"
        payload = {'component': sonar_component, 'metricKeys': metricKeys_string}

        # get sonar data
        Log.log_message("autoWeeklyData", "[INFO] GET Sonar URL: %s, PAYLOAD: %s", component_url, json.dumps(payload))
        resp = requests.get(url=component_url, params=payload, auth=(self.token, ""))

        if resp:
            result_resp = resp.json()
            Log.log_message("autoWeeklyData", "[INFO] Sonar Data: %s", json.dumps(result_resp))
        else:
            Log.log_message("autoWeeklyData", "[WARNING] Sonar Data: none")
            return None

        # clean response to dict['字段名': value]
        measures = result_resp.get('component', "").get('measures', "")
        if isinstance(measures, list):
            for measure in measures:
                if measure.get('metric', "") in sonar_metricKeys:
                    result[measure.get('metric', "")] = measure.get('value', 0)
        else:
            return None

        return result


# test
if __name__ == "__main__":

    sonar_test = SonarHandel("http://sonar.mobvista.com",
                             "37c1a27d3ffcbf0e722a061d0964bd3c0c2813ab")

    result = sonar_test.get_component_data("m-doraemon", ["bugs", "code_smells", "duplicated_lines_density"])

    print(result)
