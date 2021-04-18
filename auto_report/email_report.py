#!/usr/bin/python
# coding=utf-8
"""
@author: qyke
发信
"""
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from auto_report.logger import Log


class EamilHandel:
    def __init__(self, host, user, pwd, s_port=25):
        """
        :param host: smtp server host
        :param user:
        :param pwd:
        :param port s_smtp端口号
        """
        self.smtpObj = smtplib.SMTP(host, s_port)
        # self.smtpObj.set_debuglevel(1)
        self.smtpObj.login(user, pwd)

    def sendmail(self, sender, receivers, subject, message_html):
        """
        :param sender: string
        :param receivers: list
        :param subject: string
        :param message_html: html format message
        :return: bool
        """
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        s = "%04d%02d%02d" % (year, month, day)

        message = MIMEText(message_html, 'html', 'utf-8')
        message['From'] = Header(sender)
        message['to'] = Header(';'.join(receivers))
        message['Subject'] = Header(subject + "-" + s, 'utf-8')
        try:
            self.smtpObj.sendmail(sender, receivers, message.as_string())
            Log.log_message("autoWeeklyData", "[INFO] Send email success to %s" % message['to'])
        except smtplib.SMTPException as e:
            Log.log_message("autoWeeklyData", "[ERROR] Send email failer: %s", e)


# test
if __name__ == '__main__':
    body = r'<style class="fox_global_style"> div.fox_html_content { line-height: 1.5;} /* 一些默认样式 */ blockquote { margin-Top: 0px; margin-Bottom: 0px; margin-Left: 0.5em } ol, ul { margin-Top: 0px; margin-Bottom: 0px; list-style-position: inside; } p { margin-Top: 0px; margin-Bottom: 0px } </style><div><table class="relative-table wrapped confluenceTable tablesorter tablesorter-default stickyTableHeaders"  rules="rows" resolved="" style="border-collapse: collapse; margin: 0px; overflow-x: auto; color: rgb(23, 43, 77); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, Oxygen, Ubuntu, &quot;Fira Sans&quot;, &quot;Droid Sans&quot;, &quot;Helvetica Neue&quot;, sans-serif; font-size: 14px; letter-spacing: 0px; width: 502.588px; padding: 0px;"><colgroup><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"></colgroup><thead class="tableFloatingHeaderOriginal"><tr class="tablesorter-headerRow"><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">模块</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">Sonar Bug</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">Sonar&nbsp;<span style="margin-top: 0.2px; color: rgb(68, 68, 68);">Code Smells</span></div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">Sonar 代码重复</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">白盒覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">黑盒覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">备注</div></th></tr></thead><tbody>'

    body2 = r'<tr role="row"><td colspan="1" class="confluenceTd">ADX</td><td colspan="1" class="confluenceTd">0</td><td colspan="1" class="confluenceTd">-</td><td colspan="1" class="confluenceTd">-</td><td colspan="1" class="confluenceTd">44%</td><td colspan="1" class="confluenceTd">65%</td><td colspan="1" class="confluenceTd">-</td></tr>'

    body3 = r'</tbody></table></div>'

    test_email = EamilHandel("smtp.exmail.qq.com", "qingyue.ke@mobvista.com", "9FqNb9HC8CQRmzKf", 25)

    test_email.sendmail("qingyue.ke@mobvista.com", ["mtg_qa@mintegral.com"], "【周报-CI】数据汇总", body+body2+body3)