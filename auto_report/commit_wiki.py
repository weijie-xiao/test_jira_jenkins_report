#!/usr/bin/python
# coding=utf-8
"""
@author: qyke
将数据结果写入 wiki
"""

import time
import json
import requests
from auto_report.logger import Log


class CommitWiki:
    def __init__(self, wiki_host, wiki_auth,  parent_page, wiki_pace="QA"):
        """
        :param wiki_host: string wiki地址
        :param wiki_auth: tuple (用户, 密码)
        :param parent_page: int 父目录id
        """
        self.host = wiki_host.strip("/")
        self.ancestors = parent_page
        self.type = "page"  # 类型
        self.pace = wiki_pace  # 空间名
        self.auth = wiki_auth

        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        s = "%04d%02d%02d" % (year, month, day)
        self.title = "auto_weekly_" + s
        self.id = 0
        self.version = 0
        self.find_page()

    def commit(self, content):
        """
        :param content: string 提交内容
        :return: bool true/false
        """
        commit_url = self.host + "/rest/api/content"

        # 拼装body
        commit_body = {
            "type": "page",
            "title": self.title,
            "space": {
                "key": self.pace
            },
            "ancestors": [{"id": self.ancestors}],
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }

        # creative pages use post
        my_request_handel = requests.post

        if self.id:
            commit_url = commit_url + "/" + str(self.id)
            commit_body['id'] = self.id
            commit_body['version'] = {"number": int(self.version) + 1}
            # update pages use put
            my_request_handel = requests.put

        Log.log_message("autoWeeklyData", "[INFO] COMMIT Confluence URL: %s, Body: %s", commit_url,
                        json.dumps(commit_body))

        headers = {
                "Content-Type": "application/json",
        }

        # commit 请求
        resp = my_request_handel(url=commit_url, data=json.dumps(commit_body), auth=self.auth, headers=headers)

        # 解析结果page id
        try:
            resp_json = resp.json()
        except(Exception):
            Log.log_message("autoWeeklyData", "[INFO] COMMIT Confluence resp.json() False, Title: %s", self.title)
            return False

        if resp_json:
            self.id = int(resp_json.get("id", 0))

        if self.id:
            Log.log_message("autoWeeklyData", "[INFO] COMMIT Confluence Success, Page Id: %d", self.id)
            return True
        else:
            Log.log_message("autoWeeklyData", "[INFO] COMMIT Confluence False, Title: %s", self.title)
            return False

    def find_page(self):
        """
        https://developer.atlassian.com/server/confluence/confluence-rest-api-examples/
        :return: int  page_id
        """
        find_url = self.host + "/rest/api/content"
        payload = {'title': self.title, 'spaceKey': self.pace}
        Log.log_message("autoWeeklyData", "[INFO] Find Page GET Confluence URL: %s, PAYLOAD: %s", find_url, json.dumps(payload))
        resp = requests.get(url=find_url, params=payload, auth=self.auth)
        try:
            resp_json = resp.json()
        except(Exception):
            Log.log_message("autoWeeklyData", "[WARING] Find Page ERROR %s", resp)
            return
        results = resp_json.get('results', '')
        if results and isinstance(results, list):
            self.id = int(results[0].get("id", 0))

            history_url = find_url + '/' + str(self.id) + "/history"
            resp = requests.get(url=history_url, auth=self.auth)
            self.version = resp.json().get("lastUpdated", dict()).get("number", 0)

            Log.log_message("autoWeeklyData", "[INFO] Find Page Title exit[id: %d]: %s, version: %d",
                            self.id, self.title, self.version)

    def clear(self, interval):
        start_time = time.time() - interval*86400
        find_url = self.host + "/rest/api/content"
        clear_url = self.host + "/rest/api/content"
        end = 14
        while 1:
            clear_time = time.strftime("auto_weekly_%Y%m%d", time.localtime(start_time))
            # 查找需要删除的report title
            payload = {'title': clear_time, 'spaceKey': self.pace}
            resp = requests.get(url=find_url, params=payload, auth=self.auth)
            try:
                resp_json = resp.json()
            except Exception:
                Log.log_message("autoWeeklyData", "[WARING] Find Page ERROR %s", resp)
                return
            results = resp_json.get('results', '')
            # 如果存在, 进行删除
            if results and isinstance(results, list):
                clear_id = int(results[0].get("id", 0))
                c_resp = requests.delete(url=clear_url+"/"+str(clear_id), auth=self.auth)
                Log.log_message("autoWeeklyData", "[INFO] Delete page[id:%s], response[code:%d]",
                                clear_time, c_resp.status_code)
                # 如果是周五, 开始一周间隔的删除
                if time.localtime(start_time)[6] == 4:
                    start_time -= 86400 * 7
                else:
                    start_time -= 86400
                end = 14
            # 如果不存在, 查找下一天, 重试14次后退出
            else:
                if end >= 0:
                    start_time -= 86400
                    end -= 1
                    continue
                break

# test
if __name__ == "__main__":
    body = r'<div class="table-wrap"><table class="relative-table wrapped confluenceTable tablesorter tablesorter-default stickyTableHeaders" style="letter-spacing: 0px; width: 44.542%; padding: 0px;" role="grid" resolved=""><colgroup><col style="width: 13.0682%;"></col><col style="width: 11.3337%;"></col><col style="width: 18.2203%;"></col><col style="width: 15.2672%;"></col><col style="width: 11.7037%;"></col><col style="width: 11.7016%;"></col><col style="width: 18.7053%;"></col></colgroup><thead class="tableFloatingHeaderOriginal"><tr role="row" class="tablesorter-headerRow"><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="0" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="模块: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">模块</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="1" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Sonar Bug: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Sonar Bug</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Sonar Code Smells: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Sonar <span style="color: rgb(68,68,68);">Code Smells</span></div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="3" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Sonar 代码重复: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Sonar 代码重复</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="4" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="白盒覆盖率: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">白盒覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="5" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="黑盒覆盖率: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">黑盒覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="6" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="备注: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">备注</div></th></tr></thead><thead class="tableFloatingHeader" style="display: none;"><tr role="row" class="tablesorter-headerRow"><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="0" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="模块: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">模块</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="1" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Sonar Bug: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Sonar Bug</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Sonar Code Smells: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Sonar <span style="color: rgb(68,68,68);">Code Smells</span></div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="3" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Sonar 代码重复: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Sonar 代码重复</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="4" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="白盒覆盖率: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">白盒覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="5" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="黑盒覆盖率: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">黑盒覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="6" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="备注: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">备注</div></th></tr></thead><tbody aria-live="polite" aria-relevant="all">'

    body2 = r'<tr role="row"><td colspan="1" class="confluenceTd">ADX</td><td colspan="1" class="confluenceTd">0</td><td colspan="1" class="confluenceTd">-</td><td colspan="1" class="confluenceTd">-</td><td colspan="1" class="confluenceTd">44%</td><td colspan="1" class="confluenceTd">65%</td><td colspan="1" class="confluenceTd">-</td></tr>'

    body3 = r'</tbody></table></div>'
    test_wiki_commit = CommitWiki("http://confluence.mobvista.com", ('qingyue.ke', 'Ke12345678'), 21465364)
    result = test_wiki_commit.commit(body+body2+body3)
    print(result)
