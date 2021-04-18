#!/usr/bin/python
# coding=utf-8
"""
Created on 2020年04月11日
@author: qyke
git 接口类
"""
import time
import requests
from auto_report.logger import Log
from urllib.parse import quote_plus, urlencode


class GitHandle:
    def __init__(self, hub_host, hub_auth):
        """
        :param hub_host: string
        :param hub_auth: git private token
        """
        self.url = hub_host
        self.auth = hub_auth

    def get_tag_list(self, project_name, limit=0):
        """
        :param project_name: project
        :param limit: int order by ctime desc limit
        :return: list
        """
        project_name = project_name.strip('/').strip()
        project_name = quote_plus(project_name)
        tag_url = self.url + '/api/v3/projects/' + project_name + '/repository/tags'
        auth_token = 'private_token=' + self.auth
        tag_url = tag_url + '?' + auth_token
        # get
        resp = requests.get(url=tag_url)

        if resp.status_code != 200:
            Log.log_message("autoWeeklyData", "[ERROR] get_tag_list, status code: %s", resp.status_code)
            return []

        resp_json = resp.json()

        tag_time_list = list()

        for tags in resp_json:
            ctime = tags.get("commit").get("committed_date")
            tag_time_list.append((tags.get("name"), ctime))

        if len(tag_time_list) > 1:
            tag_time_list = sorted(tag_time_list, key=lambda x: x[1], reverse=True)

        tag_list = [key[0] for key in tag_time_list]

        if limit > 0:
            tag_list = tag_list[0:limit]

        if len(tag_list) > 0:
            return tag_list
        else:
            # logger.warning("git handle, resp: None")
            print("git handle, resp: None")
            return []

    def get_last_active_projects(self, groups_name, start):
        """
        :param groups_name: []
        :param start: since format  YYYY-MM-DD
        :return: project_name_list
        """

        project_name_list = []

        for group in groups_name:

            header = {"PRIVATE-TOKEN": self.auth}

            param = {"simple": 1,
                      "order_by": "last_activity_at",
                      "per_page": 100}

            group_url = self.url + '/api/v4/groups/' + group + '/projects'
            group_url = group_url + '?' + urlencode(param)

            resp = requests.get(headers=header, url=group_url)

            if resp.status_code != 200:
                Log.log_message("autoWeeklyData", "[ERROR] group[%s], get_last_active_project, status code: %s",
                                group, resp.status_code)
                continue

            resp_json = resp.json()

            for project in resp_json:
                last_activity_at = project.get("last_activity_at", 0)
                last_activity_at = time.strptime(last_activity_at.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                last_activity_at = time.strftime("%Y-%m-%d", last_activity_at)
                if last_activity_at < start:
                    break
                if project.get("path_with_namespace", ""):
                    project_name_list.append(project.get("path_with_namespace", ""))
                else:
                    continue
        return project_name_list

    def get_commit_history(self, project_name, start, end=0):
        """
        :param project_name: git project
        :param start: since format  YYYY-MM-DD
        :param end: since format  YYYY-MM-DD
        :return: map{author: {commit_list:[], total:0}}
        """
        project_name_raw = project_name
        project_name = project_name.strip('/').strip()
        project_name = quote_plus(project_name)

        header = {"PRIVATE-TOKEN": self.auth}

        param = {"action": "pushed",
                 "after": start,
                 "per_page": 100}

        if end:
            param["before"] = end

        envent_url = self.url + '/api/v4/projects/' + project_name + '/events'
        # auth_token = 'private_token=' + self.auth
        envent_url = envent_url + '?' + urlencode(param)
        # get
        # todo 分页查询 per_page
        resp = requests.get(headers=header, url=envent_url)

        if resp.status_code != 200:
            Log.log_message("autoWeeklyData", "[ERROR] project[%s], get_commit_history, status code: %s",
                            project_name, resp.status_code)
            return {}

        envent_json = resp.json()
        author_commit = {}
        if len(envent_json) > 0:
            for envent in envent_json:
                # 动作只取pushed
                if not envent.get('action_name', '') in ['pushed to', 'pushed new']:
                    continue

                push_data = envent.get('push_data', 0)

                # commit_title 里面有Merge的，不记录
                if not push_data \
                        or not push_data.get('commit_title', '') \
                        or "Merge branch" in push_data.get('commit_title', ''):
                    continue

                author_username = envent.get('author_username', '')
                if not author_username:
                    continue

                if not (author_username in author_commit):
                    author_commit[author_username] = {"project": project_name_raw, "commit_list": [], "total": 0}

                # 获取commit sha
                commit_to = push_data.get('commit_to', 0)
                if not commit_to:
                    continue

                # 有重复commit sha
                if commit_to in author_commit[author_username]["commit_list"]:
                    continue

                author_commit[author_username]["commit_list"].append(commit_to)
                # 只拿additions的数据
                add = self.get_commit_line(project_name, commit_to).get("additions", 0)
                author_commit[author_username]["total"] += add
                Log.log_message("autoWeeklyData",
                                "[INFO] get_commit_history project[%s], author[%s], commit[%s], additions[%s]",
                                project_name_raw, author_username, commit_to, add)

        return author_commit

    def get_commit_line(self, project_name, commit_sha):
        """
        :param project_name:
        :param commit_sha
        :return: stats{additions:, deletions:, total:}
        """

        commit_url = self.url + '/api/v4/projects/' + project_name + '/repository/commits/' + commit_sha
        stats = {}
        header = {"PRIVATE-TOKEN": self.auth}
        resp = requests.get(url=commit_url, headers=header)
        if resp.status_code != 200:
            Log.log_message("autoWeeklyData", "[ERROR] project[%s], get_commit_line[%s], status code: %s",
                            project_name, commit_sha, resp.status_code)
            return stats
        resp_json = resp.json()

        if len(resp_json.items()) > 0:
            stats = resp_json.get("stats", {})

        return stats


# test
if __name__ == "__main__":
    GitHandle_obj = GitHandle('http://gitlab.mobvista.com', "XyPnsM99h9fmet_JGyFM")
    #taglist = GitHandle_obj.get_tag_list('ADN/adnet', 5)

    print(GitHandle_obj.get_commit_history('ADN/adx', '2020-04-03'))
