#!/usr/bin/python
# coding=utf-8
"""
@author: qyke
获取jenkins 项目数据
"""

import json
import re
import requests
from requests_html import HTMLSession
from auto_report.logger import Log


class JenkinsHandel:
    def __init__(self, jenkins_host, jenkins_auth):
        """
        :param jenkins_host: string jenkins host
        :param jenkins_auth: tuple jenkins auth
        """
        self.url = jenkins_host.strip('/')
        self.auth = jenkins_auth

    def last_success_build_id(self, project_name, job_name, git_branch, single_pipeline=False):
        """
        :param project_name: string pipeline名称
        :param job_name: string job名称
        :param git_branch: string 远程库git branch name
        :return: int 该branch 最后一次成功构建结果id
        """

        # get jenkins build id
        job_name = job_name.strip()

        if single_pipeline:
            project_name = job_name.split('.')[0]
            job_name = job_name.split('.')[1]
            last_build_url = self.url + '/job/' + project_name + \
                         '/lastSuccessfulBuild/api/json?depth=3'
        else:
            last_build_url = self.url + '/job/' + project_name + '/job/' + str(git_branch).strip() +\
                         '/lastSuccessfulBuild/api/json?depth=3'

        # get
        Log.log_message("autoWeeklyData", "[INFO] GET Jenkins build_id URL: %s", last_build_url)

        # dsp 黑盒没有在pipeline中, 写特殊逻辑直接获取 -----------------
        # if job_name == "Deploy-Dsp-Server-Grey":
        #     last_build_url = self.url + '/job/' + job_name + '/lastSuccessfulBuild/api/json?depth=3'
        #     resp = requests.get(url=last_build_url, auth=self.auth)
        #
        #     if resp:
        #         result_resp_json = resp.json()
        #         Log.log_message("autoWeeklyData", "[INFO] Jenkins Build Data: %s", json.dumps(result_resp_json))
        #     else:
        #         Log.log_message("autoWeeklyData", "[WARNING] Jenkins Build Data: none")
        #         return None
        #
        #     return int(result_resp_json.get("id", None))

        resp = requests.get(url=last_build_url, auth=self.auth)

        if resp:
            result_resp_string = json.dumps(resp.json())
            Log.log_message("autoWeeklyData", "[INFO] Jenkins Build Data: %s", result_resp_string)
        else:
            Log.log_message("autoWeeklyData", "[WARNING] Jenkins Build Data: none")
            return None

        #  获取最后一次成功构建结果id

        build_id = 0
        build_id_re = re.finditer(r'"description": "%s #(?P<build_id>\d+)"' % (job_name,), result_resp_string)

        for build_ids in build_id_re:
            build_id = int(build_ids.groupdict()['build_id'])
            break
        # build_id = result_resp.get('buildsByBranchName', '').get(git_branch, '').get('buildNumber', 0)
        if build_id:
            return int(build_id)
        else:
            return None

    def get_cloverphp(self, job_name, build_id, single_pipeline=False):
        """
        get jenkins cloverphp 类型覆盖率
        :param job_name: string 项目名称
        :param build_id: int build id
        :return: float 覆盖率%
        """
        session = HTMLSession()
        if single_pipeline:
            job_name = job_name.split('.')[1]
        status_url = self.url + '/job/' + job_name + '/' + str(build_id)

        # get
        Log.log_message("autoWeeklyData", "[INFO] GET Jenkins Cover URL: %s", status_url)
        resp = session.get(url=status_url, auth=self.auth)
        Log.log_message("autoWeeklyData", "[INFO] GET Jenkins Cover Response : %s", resp)

        # 获取指定build id cloverphp-report cover
        cover = resp.html.search("Clover Code Coverage - {cover}% ")

        cover_ratio = 0.0
        if cover:
            try:
                cover_ratio = round(float(cover['cover']), 2)
                Log.log_message("autoWeeklyData", "[INFO] Jenkins cloverphp cover_ratio: %f", cover_ratio)
                return cover_ratio
            except(Exception):
                Log.log_message("autoWeeklyData", "[WARNING] Jenkins cloverphp cover_ratio: None")
                return None

    def get_cobertura(self, job_name, build_id, single_pipeline=False):
        """
        get jenkins cobertura 类型覆盖率
        :param job_name: string 项目名称
        :param build_id: int build id
        :return: float 覆盖率%
        """

        job_name = job_name.strip()
        if single_pipeline:
            job_name = job_name.split('.')[1]

        cobertura_url = self.url + '/job/' + job_name + '/' + str(build_id) + '/cobertura/api/json?depth=2'

        # get
        Log.log_message("autoWeeklyData", "[INFO] GET Jenkins cobertura URL: %s", cobertura_url)
        resp = requests.get(url=cobertura_url, auth=self.auth)

        if resp:
            result_resp = resp.json()
            Log.log_message("autoWeeklyData", "[INFO] Jenkins cobertura Data: %s", json.dumps(result_resp))
        else:
            Log.log_message("autoWeeklyData", "[WARNING] Jenkins cobertura Data: none")
            return None

        #  获取指定build id cobertura类型覆盖率
        elements = result_resp.get('results', '').get('elements', '')

        cover_ratio = 0.0

        # 遍历elements 获取Lines 覆盖率
        if elements and isinstance(elements, list):
            for element in elements:
                if element.get('name', '') == "Lines":
                    cover_ratio = element.get('ratio', 0)
                    Log.log_message("autoWeeklyData", "[INFO] Jenkins cobertura cover_ratio: %f", float(cover_ratio))
                    return round(float(cover_ratio), 2)
        else:
            Log.log_message("autoWeeklyData", "[WARNING] Jenkins cobertura cover_ratio: None")
            return None


# test
if __name__ == "__main__":

    jenkins_test = JenkinsHandel("http://ci.mobvista.com", ('qingyue.ke', 'Ke123456789'))
    # build_id = jenkins_test.last_success_build_id("M-Adx-WhiteBox-Test", "master")
    # cover_rate = jenkins_test.get_cobertura("M-Adx-WhiteBox-Test", build_id)
    #print(cover_rate)
    build_id_t = jenkins_test.last_success_build_id("M-Mintegral-Pipeline", "M-MG-ApiTest-k8s.M-MG-ApiTest-report", "master", True)
    cover_rate_t = jenkins_test.get_cloverphp("M-MG-ApiTest-k8s.M-MG-ApiTest-report", build_id_t, True)
    print(cover_rate_t)
