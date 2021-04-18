#!/usr/bin/python
# coding=utf-8
"""
@author: qyke
输出cover report 结果
"""

from auto_report import config
from auto_report.logger import Log
from auto_report.sonar_data_aly import SonarHandel
from auto_report.jenkins_data_aly import JenkinsHandel


class CoverReport:
    def __init__(self, jenkins: JenkinsHandel, sonar: SonarHandel, project_map):
        """
        :param jenkins: JenkinsHandel
        :param sonar: SonarHandel
        """
        self.jenkins = jenkins
        self.sonar = sonar
        self.project_report = project_map
        self.report_commit = ''

    def run(self):

        self.get_sonar_data()
        self.get_jenkins_data()

    def get_sonar_data(self):
        # 遍历project map 将sonar 数据写入project_map
        for pro_key, pro_value in self.project_report.items():
            sonar_report = pro_value.get('sonar_report', "")
            if not sonar_report:
                continue
            sonar_pro = sonar_report.get('project_name', "")
            sonar_metricKeys = sonar_report.get('metricKeys', "")
            result = dict()
            # 进行一次project 的sonar 获取
            Log.log_message("autoWeeklyData", "[INFO] Analyze sonar project:[%s]:", sonar_pro)
            if sonar_report and sonar_pro and sonar_metricKeys:
                result = self.sonar.get_component_data(sonar_pro, sonar_metricKeys)
                sonar_date_list = list()
                for key in sonar_metricKeys:
                    if key == 'duplicated_lines_density':
                        v = str(result.get(key, '-')) + "%"
                    else:
                        v = str(result.get(key, '-'))
                    sonar_date_list.append(v)
                # 结果放入project_map
                tmp = self.project_report[pro_key]
                tmp_s = tmp["sonar_report"]
                tmp_s["metricData"] = sonar_date_list
        return

    def get_jenkins_data(self):
        # 遍历project map 将jenkins 数据写入project_map
        for pro_key, pro_value in self.project_report.items():
            cover_report = pro_value.get('cover_report', "")
            if not cover_report:
                continue
            cover_jobs = cover_report.get('project_name', [])
            cover_type = cover_report.get('cover_report_type', "cobertura").strip()

            result = dict()
            # 进行一次project 的cover 获取
            Log.log_message("autoWeeklyData", "[INFO] Analyze jenins project:[%s]:", ",".join(cover_jobs))
            if cover_report and cover_jobs and cover_type:
                for job in cover_jobs:
                    if not job:
                        result[""] = "-"
                        continue
                    merge_report = True if len(job.split('.')) > 1 else False
                    last_success = self.jenkins.last_success_build_id(pro_key, job, "master", merge_report)
                    if cover_type == "cloverphp":
                        # self.jenkins.last_success_build_id(cover_pro, "master") 获取对应分支 最后一次成功的构建id
                        result[job] = self.jenkins.get_cloverphp(job, last_success, merge_report)
                    else:
                        result[job] = self.jenkins.get_cobertura(job, last_success, merge_report)

                cover_date_list = list()
                for key in cover_jobs:
                    cover_date_list.append(str(result.get(key, '-')) + "%")
                # 结果放入project_map
                tmp = self.project_report[pro_key]
                tmp_s = tmp["cover_report"]
                tmp_s["coverData"] = cover_date_list
        return sorted(self.project_report.items(), key=lambda x: x[1].get('id', -1))

    def commit_report(self):
        body2 = ""
        project_report_list = sorted(self.project_report.items(), key=lambda x: x[1].get('id', -1))
        for pro_key, pro_value in project_report_list:
            body2 += r'<tr role="row">'
            commit_project_name = pro_key
            body2 += r'<td colspan="1" class="confluenceTd">%s</td>' % (commit_project_name,)
            sonar_report = pro_value.get('sonar_report', "")
            if sonar_report:
                sonar_metricData = sonar_report.get('metricData')
            else:
                sonar_metricData = ["-", "-", "-"]

            for data in sonar_metricData:
                body2 += r'<td align="center" colspan="1" class="confluenceTd">%s</td>' % (data,)

            cover_report = pro_value.get('cover_report', "")
            if cover_report:
                cover_data = cover_report.get('coverData')
            else:
                cover_data = ["-", "-"]

            for data in cover_data:
                body2 += r'<td  align="center" colspan="1" class="confluenceTd">%s</td>' % (data,)

            body2 += r'<td colspan="1" class="confluenceTd"><br></br></td></tr>'

        # self.report_commit = config.wiki_template['body_header'] + body2 + config.wiki_template['body_end']

        return config.wiki_template['body_title'] + config.wiki_template['body_header'] + body2 + config.wiki_template['body_end']

        # self.wiki.commit(config.wiki_template['body_header'] + body2 + config.wiki_template['body_end'])

        # 发送邮件
        # if len(config.emain_receive) > 0:
        #     self.email.sendmail(config.email_user,
        #                         config.emain_receive,
        #                         "【QA-CI周报】数据汇总",
        #                         config.email_template['body_header'] + body2 + config.email_template['body_end'])
