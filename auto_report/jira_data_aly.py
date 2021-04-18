#!/usr/bin/python
# coding=utf-8
"""
Created on 2018年08月16日
@author: qyke
jira 接口类
"""
import re
import time
from typing import List
from urllib.parse import quote

from jira import JIRA

from auto_report.logger import Log

tag_re = re.compile(r'(?P<git>git@gitlab.mobvista.com:[\w\.\/\_]+\.git) (?P<tag>[\w\.\/\_]+)')


class HandleJira:

    def __init__(self, url, name, pwd):
        """
        :param url:  jira url
        :param name:
        :param pwd:
        """
        # 持久化jira
        self.jira = JIRA(server=url,
                         auth=(name, pwd))

    def add_comment(self, key, body):
        """
        :param body: str
        :return:
        """
        self.jira.add_comment(key, body)  # 写入commit

    def status(self, key):

        issue = self.jira.issue(key)  # 重新载入issue
        status = issue.fields.status.name

        return str(status)  # 返回issue 状态

    def fix_version(self, key):

        issue = self.jira.issue(key)  # 重新载入issue
        version_list = issue.fields.fixVersions

        version_name_list = [str(v.name) for v in version_list]

        return version_name_list  # 返回issue 修复版本

    def get_tags(self, key):
        """
        :return: list [{'git':'','tag':''}]
        """
        issue = self.jira.issue(key)  # 重新载入issue
        tags = issue.fields.customfield_10714
        tags = tag_re.finditer(tags)
        tag_list = [i.groupdict() for i in tags]
        return tag_list

    def transitions(self, key, trans_name, trans_field=None):
        """
        :param key jira key name
        :param trans_name:str 需要变更的事件名
        :param trans_field:dict 附加参数
        :return: result
        """
        issue = self.jira.issue(key)

        transitions = self.jira.transitions(issue)  # 获取issue可执行事件

        action_id = 0

        for t in transitions:
            if t['name'].strip() == trans_name.strip():
                action_id = int(t['id'])  # 查找事件id

        if action_id:
            try:
                # 变更jira issue 状态
                self.jira.transition_issue(issue, action_id, fields=trans_field)
                result = 1
            except Exception as e:
                # logger.error("jira issue failed: [%s], fields: [%s]" % (self.key, trans_field))
                # logger.error(e)
                Log.log_message("autoWeeklyData", "[ERROR] jira issue failed: [%s], fields: [%s]", key, trans_field)
                Log.log_message("autoWeeklyData", e)
                result = 0
        else:
            # logger.warning("invalid trans_name: %s, jira: %s" %(trans_name, self.key))
            Log.log_message("autoWeeklyData", "[WARNING] invalid trans_name: %s, jira: %s", trans_name, key)
            result = 0

        return result

    def search_bug_by_assignee(self, assignees: List, start, end=0):

        """
        :param assignees: 经办人_list
        :param start: 开始时间 format  YYYY-MM-DD
        :param end: 结束时间 format  YYYY-MM-DD
        :return: assignee_bug{ author:{keys:[], total:0}}
        """

        if 'root' in assignees:
            assignees.pop(assignees.index("root"))
        assignees_str = ",".join(assignees)

        if not end:
            end = time.strftime("%Y-%m-%d", time.localtime(time.time()))

        jql_str = 'issuetype = Bug ' \
                  'AND assignee in (%s) ' \
                  'AND created >= %s AND created <= %s ' \
                  'AND summary !~ "jenkins PIPELINE" ' \
                  'ORDER BY assignee ASC' % \
                  (assignees_str, start, end)

        result = self.jira.search_issues(jql_str=jql_str, fields="key, assignee", maxResults=500, json_result=True)
        # todo maxResults分页查询

        # assignee_bug = {}
        assignee_project_bug = {}
        for issues in result.get("issues", []):
            try:
                key = issues["key"]
                project = self.get_project_detail(key.split("-")[0])
                assignee = issues["fields"]["assignee"]["key"]
                assignee = assignee.split("@")[0]
            except Exception as e:
                Log.log_message("autoWeeklyData", "[ERROR] jira search_bug_by_assignee failed: %s, issues: %s", e,
                                issues)
                continue

            if assignee not in assignee_project_bug:
                # assignee_bug[assignee] = {}
                assignee_project_bug[assignee] = {}
            if project not in assignee_project_bug[assignee]:
                assignee_project_bug[assignee][project] = {"keys": [], "total": 0}

            # assignee_bug[assignee]["keys"].append(key)
            # assignee_bug[assignee]["total"] += 1

            assignee_project_bug[assignee][project]["keys"].append(key)
            assignee_project_bug[assignee][project]["total"] += 1

        return assignee_project_bug, quote(jql_str)

    def get_project_detail(self, project_key):
        projects = self.jira.project_components(project_key)
        # print(projects[0].raw)
        git_project_name = projects[0].raw.get("description").split(":")[-1].rstrip(".git")
        return git_project_name


# test
if __name__ == '__main__':
    JIRA_CONFIG = {
        'url': 'https://jira.mobvista.com',
        'name': 'qa_auto_test',
        'pwd': 'pBlvjyXO7dhSDtUd'
    }

    J = HandleJira(JIRA_CONFIG['url'], JIRA_CONFIG['name'], JIRA_CONFIG['pwd'])

    start = time.localtime(time.time() - 86400 * 30)
    # print(J.search_bug_by_assignee(["zhihao.lin"], "%s-%s-%s" % (start[0], start[1], start[2])))
    print(J.get_project_detail("SSFRONT"))
