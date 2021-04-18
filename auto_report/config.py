jenkins_host = "http://ci.mobvista.com"
jenkins_auth = ('qa_auto_test', 'pBlvjyXO7dhSDtUd')

wiki_host = "https://confluence.mobvista.com"
wiki_auth = ('qa_auto_test', 'pBlvjyXO7dhSDtUd')
wiki_ancestors = 21465364  # 父级目录

sonar_host = "http://sonar.mobvista.com"
sonar_token = "37c1a27d3ffcbf0e722a061d0964bd3c0c2813ab"

email_host = "smtp.exmail.qq.com"
email_user = ""
email_pwd = "9FqNb9HC8CQRmzKf"
emain_receive = [""]

jira_url = 'http://jira.mobvista.com'
jira_name = 'qa_auto_test'
jira_pwd = 'pBlvjyXO7dhSDtUd'

git_host = "http://gitlab.mobvista.com/"
git_name = "mtg_qa"
git_token = "XyPnsM99h9fmet_JGyFM"
git_project_list = ["ADN"]

project_map = {
    "M-adnet-Pipeline": {
        "id": 1,
        "sonar_report": {
            "project_name": "m-adnet",
            "metricKeys": ["bugs", "code_smells", "duplicated_lines_density"]
        },
        "cover_report": {
            "project_name": ["M-Adnet-WhiteBox-Test", "M-Adnet-HB-BlackBox-Test-K8s.M-Adnet-HB-BlackBox-Report"],
            "cover_report_type": "cobertura"
        }
    },
    "M-AdnTask-Pipeline": {
        "id": 5,
        "sonar_report": {
            "project_name": "m-adnTask",
            "metricKeys": ["bugs", "code_smells", "duplicated_lines_density"]
        },
        "cover_report": {
            "project_name": ["M-AdnTask-WhiteBox-Test", ""],
            "cover_report_type": "cloverphp"
        }
    },
    "M-AdnTracking-Pipeline": {
        "id": 3,
        "sonar_report": {
            "project_name": "m-adntracking",
            "metricKeys": ["bugs", "code_smells", "duplicated_lines_density"]
        },
        "cover_report": {
            "project_name": ["M-Adntracking-WhiteBox-Test", "M-AdnTrackingTest-New"],
            "cover_report_type": "cobertura"
        }
    },
    "M-Adx-Pipeline": {
        "id": 2,
        "sonar_report": {
            "project_name": "m-adx",
            "metricKeys": ["bugs", "code_smells", "duplicated_lines_density"]
        },
        "cover_report": {
            "project_name": ["M-Adx-WhiteBox-Test", "M-AdxTest"],
            "cover_report_type": "cobertura"
        }
    },
    "M-AdxTracking-Pipeline": {
        "id": 3,
        "sonar_report": {
            "project_name": "m-adxtracking",
            "metricKeys": ["bugs", "code_smells", "duplicated_lines_density"]
        },
        "cover_report": {
            "project_name": ["M-Adxtracking-WhiteBox-Test-New", "M-AdxTrackingTest-New"],
            "cover_report_type": "cobertura"
        }
    },
    "M-doraemon-Pipeline": {
        "id": 6,
        "sonar_report": {
            "project_name": "m-doraemon",
            "metricKeys": ["bugs", "code_smells", "duplicated_lines_density"]
        },
        "cover_report": {
            "project_name": ["M-Doraemon-WhiteBox-Test-k8s", "M-Doraemon-Test-k8s"],
            "cover_report_type": "cloverphp"
        }
    },
    "M-Mintegral-Pipeline": {
        "id": 4,
        "sonar_report": {
            "project_name": "m-mg-api",
            "metricKeys": ["bugs", "code_smells", "duplicated_lines_density"]
        },
        "cover_report": {
            "project_name": ["", "M-MG-ApiTest-k8s.M-MG-ApiTest-report"],
            "cover_report_type": "cloverphp"
        }
    },
    "Dsp_pipeline": {
        "id": 7,
        "sonar_report": {
            "project_name": "mvdsp",
            "metricKeys": ["bugs", "code_smells", "duplicated_lines_density"]
        },
        "cover_report": {
            "project_name": ["Deploy-Dsp-PIPELine-White-Test", "Deploy-Dsp-PIPELine-System-Test"],
            "cover_report_type": "cobertura"
        }
    },
    "AdServer_Pipeline": {
        "id": 8,
        "cover_report": {
            "project_name": ["Adserver-pipeline-WhiteApiTest", "Adserver-pipeline-AutoTest"],
            "cover_report_type": "cobertura"
        }
    },
    "M-SS-Pipeline": {
        "id": 9,
        "sonar_report": {
            "project_name": "m-ss-api",
            "metricKeys": ["bugs", "code_smells", "duplicated_lines_density"]
        },
        "cover_report": {
            "project_name": ["", "M-SS-ApiTest-k8s.M-SS-ApiTest-report"],
            "cover_report_type": "cloverphp"
        }
    },
    "M-Cybertron-Pipeline": {
        "id": 10,
        "cover_report": {
            "project_name": ["M-Cybertron-WhiteBox-Test", "M-Cybertron-BlackBox-Test-k8s.M-Cybertron-BlackBox-Report"],
            "cover_report_type": "cobertura"
        }
    }
}

wiki_template = {
    "body_title": r'<div class="table-wrap"><h2 class="auto-cursor-target" id="auto_weekly">自动化覆盖率</h2>',
    "body_header": r'<div class="table-wrap"><table class="relative-table wrapped confluenceTable tablesorter tablesorter-default stickyTableHeaders" style="letter-spacing: 0px; width: 44.542%; padding: 0px;" role="grid" resolved=""><colgroup><col style="width: 13.0682%;"></col><col style="width: 11.3337%;"></col><col style="width: 18.2203%;"></col><col style="width: 15.2672%;"></col><col style="width: 11.7037%;"></col><col style="width: 11.7016%;"></col><col style="width: 18.7053%;"></col></colgroup><thead class="tableFloatingHeaderOriginal"><tr role="row" class="tablesorter-headerRow"><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="0" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="模块: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">模块</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="1" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Sonar Bug: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Sonar Bug</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Sonar Code Smells: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Sonar <span style="color: rgb(68,68,68);">Code Smells</span></div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="3" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Sonar 代码重复: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Sonar 代码重复</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="4" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="白盒覆盖率: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">白盒覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="5" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="黑盒覆盖率: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">黑盒覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="6" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="备注: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">备注</div></th></tr></thead><tbody aria-live="polite" aria-relevant="all">',
    "body_end": r'</tbody></table></div></div>'
}

email_template = {
    "body_header": r'<style class="fox_global_style"> div.fox_html_content { line-height: 1.5;} /* 一些默认样式 */ blockquote { margin-Top: 0px; margin-Bottom: 0px; margin-Left: 0.5em } ol, ul { margin-Top: 0px; margin-Bottom: 0px; list-style-position: inside; } p { margin-Top: 0px; margin-Bottom: 0px } </style><div><table class="relative-table wrapped confluenceTable tablesorter tablesorter-default stickyTableHeaders"  rules="rows"  frame=below resolved="" style="border-collapse: collapse; margin: 0px; overflow-x: auto; color: rgb(23, 43, 77); font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, Oxygen, Ubuntu, &quot;Fira Sans&quot;, &quot;Droid Sans&quot;, &quot;Helvetica Neue&quot;, sans-serif; font-size: 14px; letter-spacing: 0px; width: 600px; padding: 0px;"><colgroup><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"><col style="width: 0px;"></colgroup><thead class="tableFloatingHeaderOriginal"><tr class="tablesorter-headerRow"><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">模块</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">Sonar Bug</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">Code Smells</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">Sonar 代码重复</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">白盒 覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">黑盒 覆盖率</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" scope="col" style="border: 1px solid rgb(193, 199, 208); padding: 7px 15px 7px 10px; vertical-align: top; text-align: left; min-width: 8px; background: right center no-repeat rgb(244, 245, 247); color: rgb(23, 43, 77); cursor: pointer;"><div class="tablesorter-header-inner" style="margin: 0px; padding: 0px;">备注</div></th></tr></thead><tbody>',
    "body_end": r'</tbody></table></div>'
}

bug_template = {
    "body_title": r'<div class="table-wrap"><h2 class="auto-cursor-target" id="auto_weekly">开发质量(周期-2 weeks: %s-now )</h2>',
    "body_url": r'<div class="table-wrap"><p>统计策略: 周期内git/ADN仓库的提交代码行数, 周期内jira上bug的数量 <a class="external-link" href="%s" rel="nofollow">BUG-jira地址</a></p>',
    "body_header": r'<div class="table-wrap"><table class="confluenceTable tablesorter tablesorter-default stickyTableHeaders" role="grid" resolved="" style="padding: 0px;"><thead class="tableFloatingHeaderOriginal"><tr role="row" class="tablesorter-headerRow"><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="0" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="开发: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">开发</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="1" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="代码模块: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">代码模块</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="提交代码总数: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">提交代码总数</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="3" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Bugs: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Bugs</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="4" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="千行Bug率(参考): No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">千行Bug率(参考)</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="4" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="备注: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">备注</div></th></tr></thead><tbody aria-live="polite" aria-relevant="all">',
    "body_end": r'</tbody></table></div></div></div>'
}

special_project_for_per_user_per_project_report = ["ADN/ss_frontend", "ADN/portal_frontend", "ADN/mintegral_frontend", "ADN/adv_doc"]

project_bug_template = {
    "body_title": r'<div class="table-wrap"><h2 class="auto-cursor-target" id="auto_weekly">前端项目开发质量(分项目，周期-2 weeks: %s-now )</h2>',
    "body_url": r'<div class="table-wrap"><p>统计策略: 周期内git/ADN仓库的提交代码行数, 周期内jira上bug的数量 <a class="external-link" href="%s" rel="nofollow">BUG-jira地址</a></p>',
    "body_header": r'<div class="table-wrap"><table class="confluenceTable tablesorter tablesorter-default stickyTableHeaders" role="grid" resolved="" style="padding: 0px;"><thead class="tableFloatingHeaderOriginal"><tr role="row" class="tablesorter-headerRow"><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="0" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="开发: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">开发</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="1" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="代码模块: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">代码模块</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="提交代码总数: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">提交代码总数</div></th><th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="3" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Bugs: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">Bugs</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="4" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="千行Bug率(参考): No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">千行Bug率(参考)</div></th><th colspan="1" class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="4" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="备注: No sort applied, activate to apply an ascending sort" style="user-select: none;"><div class="tablesorter-header-inner">备注</div></th></tr></thead><tbody aria-live="polite" aria-relevant="all">',
    "body_end": r'</tbody></table></div></div></div>'
}
