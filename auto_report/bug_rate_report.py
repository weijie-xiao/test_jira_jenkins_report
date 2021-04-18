#!/usr/bin/python
# coding=utf-8
"""
@author: qyke
输出bug率 结果
"""
import time
from auto_report import config
from auto_report.logger import Log
from auto_report.git_data_aly import GitHandle
from auto_report.jira_data_aly import HandleJira


class BugRateReport:
    def __init__(self, git: GitHandle, jira: HandleJira, group_list, period):
        """
        :param git:
        :param jira:
        :param mtg组-ADN
        :param peroid 报告时间 date
        :param project_list: mtg git project list
        """
        self.git = git
        self.jira = jira
        self.project_list = group_list
        self.start_time = time.localtime(time.time() - (period+1) * 86400)
        self.author_map = {}
        self.result = []
        self.jql = ""

    def run(self):
        self.get_last_active_project()
        Log.log_message("autoWeeklyData", "[INFO] get commit start...")
        self.git_commit()
        Log.log_message("autoWeeklyData", "[INFO] get commit finish...")
        Log.log_message("autoWeeklyData", "[INFO] get bugs start...")
        self.bug_count()
        Log.log_message("autoWeeklyData", "[INFO] get bugs finish...")
        self.get_bug_rate()

    def get_last_active_project(self):
        start = self.start_time
        active_start = time.strftime("%Y-%m-%d", start)
        self.project_list = self.git.get_last_active_projects(self.project_list, active_start)
        pass

    def git_commit(self):

        # 最近两周的提交
        start = self.start_time
        commit_start = time.strftime("%Y-%m-%d", start)

        # 遍历每个git project的提交信息
        for project in self.project_list:
            Log.log_message("autoWeeklyData", "[INFO] get project[%s] commit start[%s]...", project, commit_start)
            project_commit = self.git.get_commit_history(project, commit_start)

            # 聚合author的提交信息
            for author, commit in project_commit.items():
                if author not in self.author_map:
                    self.author_map[author] = {"project_set": set(),
                                               "commit_sha": list(),
                                               "commits_total": 0,
                                               "bug_keys": [],
                                               "bugs_total": 0}

                self.author_map[author]["project_set"].add(project)
                self.author_map[author]["commit_sha"] += commit.get("commit_list", [])
                self.author_map[author]["commits_total"] += commit.get("total", 0)

            Log.log_message("autoWeeklyData", "[INFO] get project[%s] commit end...", project)

    def bug_count(self):

        author_list = []

        # 最近两周的bug
        start = self.start_time
        bug_create_time = time.strftime("%Y-%m-%d", start)

        for key, value in self.author_map.items():
            author_list.append(key)

        if len(author_list) > 0:
            author_project_bugs, jql_encode = self.jira.search_bug_by_assignee(author_list, bug_create_time)
            self.jql = jql_encode
            for author, detail in author_project_bugs.items():
                for project, bugs in detail.items():
                    self.author_map[author]["bug_keys"] += bugs.get("keys", [])
                    self.author_map[author]["bugs_total"] += bugs.get("total", 0)

    def get_bug_rate(self):
        """
        :return: [(author, commits_total, bugs_total, "{:.2f}".format(bugs_rate))] order by bugs_rate
        """
        result = []
        if len(self.author_map.items()) <= 0:
            return result

        for author, info in self.author_map.items():
            commit_project = info.get("project_set", ())
            commit_sha = info.get("commit_sha", [])
            commits_total = info.get("commits_total", 0)
            bug_keys = info.get("bug_keys", [])
            bugs_total = info.get("bugs_total", 0)
            bugs_rate = float()
            if commits_total > 0 and bugs_total > 0:
                bugs_rate = (bugs_total/commits_total) * 1000
            Log.log_message("autoWeeklyData", "[Info] author[%s], "
                                              "project_set: %s, "
                                              "commit_sha: %s, "
                                              "commits_total[%s], "
                                              "bug_keys: %s, "
                                              "bugs_total:[%s],"
                                              "bugs_rate[%s]",
                            author, commit_project,  commit_sha, commits_total, bug_keys, bugs_total, bugs_rate)

            result.append((author, ", ".join(commit_project), commits_total, bugs_total, "{:.2f}".format(bugs_rate)))

        result_sort = sorted(result, key=lambda d: d[3], reverse=True)
        for result_bug in result_sort:
            if result_bug[3] > 0:
                self.result.append(result_bug)
            else:
                break
        return self.result

    def commit_report(self):
        body2 = ""
        bugs_report_list = self.result

        start = self.start_time
        bug_start = time.strftime("%Y-%m-%d", start)

        # bugs_report_list = [('ping.wang', 'ADN/hybird', 904, 8, '8.85'), ('hongzhi.gan', 'ADN/adn_stats,ADN/adn_reporting', 643, 4, '6.22'), ('mingyang.tan', 'ADN/ss_frontend,ADN/mintegral_frontend,ADN/portal_frontend', 748, 4, '5.35'), ('zenan.liu', 'ADN/portal_api,ADN/adn_task,ADN/ss_api', 4987, 23, '4.61'), ('kangkang.wang', 'ADN/hybird', 1712, 6, '3.50'), ('shichao.mo', 'ADN/adnet,ADN/aladdin,ADN/adn_task', 274, 7, '25.55'), ('zhihong.kang', 'ADN/ss_frontend,ADN/portal_frontend', 13461, 34, '2.53'), ('ling.zhang', 'ADN/adx', 72, 1, '13.89'), ('qiangqiang.he', 'ADN/adnet,ADN/aladdin,ADN/adx', 158, 2, '12.66'), ('jiandong.wang', 'ADN/adn_reporting,ADN/mintegral,ADN/adn_task,ADN/doraemon,ADN/portal,ADN/Oauth2', 1933, 3, '1.55'), ('lihao', 'ADN/mintegral,ADN/adn_task,ADN/etl,ADN/doraemon,ADN/portal,ADN/portal_api,ADN/portal_ssp,ADN/ss_api', 2879, 3, '1.04'), ('wenbin.wei', 'ADN/adn_backend,ADN/adn_flink,wenbin.wei/aggr-layer-container,ADN/adn_fluentd_plugins,ADN/adn_data', 2783, 1, '0.36'), ('haiping.li', 'ADN/portal_api,ADN/portal_frontend,ADN/ss_api', 62, 0, '0.00'), ('xiaofa.zhong', 'ADN/adn_data', 506, 0, '0.00'), ('kaiwei.zhou', 'ADN/dididada,ADN/adn_tracking,ADN/adnet,ADN/adx_tracking,ADN/aladdin', 1358, 0, '0.00'), ('qianwen.gao', 'ADN/adn_task', 1, 0, '0.00'), ('weijie.xiao', 'ADN/portal_api,ADN/ss_api', 30, 0, '0.00'), ('ying.xie', 'ADN/luffy', 101, 0, '0.00'), ('shaoqiang.zhuang', 'ADN/adn_stats,ADN/adn_reporting', 459, 0, '0.00'), ('guixiong.ruan', 'ADN/adnet,ADN/adx_tracking,ADN/adn_tracking,ADN/adx', 8214, 0, '0.00'), ('zhaojie.yang', 'ADN/adnet,ADN/aladdin,ADN/adx', 3083, 0, '0.00'), ('lihaoming', 'ADN/adnet,ADN/adx_tracking,ADN/adx_common,ADN/adx', 830, 0, '0.00'), ('jun.wen', 'ADN/ss_api', 1, 0, '0.00'), ('root', 'ADN/adn_tracking', 2763, 0, '0.00'), ('chenggang.fu', 'ADN/adx', 115, 0, '0.00'), ('zhengguo.liu', 'ADN/adx', 5, 0, '0.00'), ('weijian.yan', 'ADN/video_transcode,ADN/adn_stats,ADN/creative,ADN/offer_sync,ADN/creative_sync', 3732, 0, '0.00'), ('ning.zhong', 'adserver/recommend_protocols', 1072, 0, '0.00'), ('xuefeng.han', 'adserver/recommend_protocols', 84, 0, '0.00'), ('yutao.sun', 'adserver/recommend_protocols', 850, 0, '0.00')]

        for author, commit_project, commits_total, bugs_total, bugs_rate in bugs_report_list:

            body2 += r'<tr role="row">'

            body2 += r'<td colspan="1" class="confluenceTd">%s</td>' % (author,)

            body2 += r'<td colspan="1" class="confluenceTd">%s</td>' % (commit_project,)

            body2 += r'<td align="center" colspan="1" class="confluenceTd">%s</td>' % (commits_total,)

            body2 += r'<td  align="center" colspan="1" class="confluenceTd">%s</td>' % (bugs_total,)

            body2 += r'<td  align="center" colspan="1" class="confluenceTd">%s%%</td>' % (bugs_rate,)

            body2 += r'<td colspan="1" class="confluenceTd"><br></br></td></tr>'

        return config.bug_template['body_title'] % (bug_start,) + \
               config.bug_template['body_url'] % (config.jira_url + "/issues/?jql=" + self.jql,) +\
               config.bug_template['body_header'] + \
               body2 + \
               config.bug_template['body_end']
