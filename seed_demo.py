#!/usr/bin/env python3
"""
WorkApp 演示数据生成脚本
模拟研发中心的企业应用中心
"""

from app import app, db
from models import User, Workbench, Workspace, AppIcon
import random

# 演示部门数据
DEPARTMENTS = {
    "研发中心": {
        "description": "汇聚研发团队所有常用工具和资源",
        "groups": {
            "开发工具": [
                {
                    "name": "GitHub",
                    "url": "https://github.com",
                    "description": "代码托管和版本控制平台"
                },
                {
                    "name": "GitLab",
                    "url": "https://gitlab.com",
                    "description": "DevOps 平台，支持 CI/CD"
                },
                {
                    "name": "VS Code",
                    "url": "https://code.visualstudio.com",
                    "description": "轻量级代码编辑器"
                },
                {
                    "name": "IntelliJ IDEA",
                    "url": "https://www.jetbrains.com/idea/",
                    "description": "Java 集成开发环境"
                },
                {
                    "name": "Postman",
                    "url": "https://www.postman.com",
                    "description": "API 测试和开发工具"
                },
                {
                    "name": "Swagger",
                    "url": "https://swagger.io",
                    "description": "API 文档生成工具"
                }
            ],
            "项目管理": [
                {
                    "name": "Jira",
                    "url": "https://www.atlassian.com/software/jira",
                    "description": "敏捷项目管理工具"
                },
                {
                    "name": "Trello",
                    "url": "https://trello.com",
                    "description": "看板式项目管理"
                },
                {
                    "name": "Asana",
                    "url": "https://asana.com",
                    "description": "团队协作和任务管理"
                },
                {
                    "name": "Confluence",
                    "url": "https://www.atlassian.com/software/confluence",
                    "description": "团队知识库和文档协作"
                },
                {
                    "name": "Notion",
                    "url": "https://www.notion.so",
                    "description": "多功能工作空间"
                },
                {
                    "name": "ClickUp",
                    "url": "https://clickup.com",
                    "description": "一体化项目管理平台"
                }
            ],
            "CI/CD": [
                {
                    "name": "Jenkins",
                    "url": "https://www.jenkins.io",
                    "description": "开源自动化服务器"
                },
                {
                    "name": "GitHub Actions",
                    "url": "https://github.com/features/actions",
                    "description": "GitHub 内置 CI/CD"
                },
                {
                    "name": "Travis CI",
                    "url": "https://travis-ci.com",
                    "description": "云端持续集成服务"
                },
                {
                    "name": "CircleCI",
                    "url": "https://circleci.com",
                    "description": "现代化 CI/CD 平台"
                },
                {
                    "name": "Docker Hub",
                    "url": "https://hub.docker.com",
                    "description": "Docker 镜像仓库"
                },
                {
                    "name": "SonarQube",
                    "url": "https://www.sonarsource.com/products/sonarqube/",
                    "description": "代码质量检测平台"
                }
            ],
            "测试工具": [
                {
                    "name": "Selenium",
                    "url": "https://www.selenium.dev",
                    "description": "Web 自动化测试框架"
                },
                {
                    "name": "Jest",
                    "url": "https://jestjs.io",
                    "description": "JavaScript 测试框架"
                },
                {
                    "name": "Cypress",
                    "url": "https://www.cypress.io",
                    "description": "前端测试框架"
                },
                {
                    "name": "BrowserStack",
                    "url": "https://www.browserstack.com",
                    "description": "跨浏览器测试平台"
                },
                {
                    "name": "Postman Collections",
                    "url": "https://www.postman.com/explore",
                    "description": "API 测试用例集合"
                },
                {
                    "name": "Lighthouse",
                    "url": "https://developers.google.com/web/tools/lighthouse",
                    "description": "网站性能分析工具"
                }
            ],
            "运维监控": [
                {
                    "name": "Grafana",
                    "url": "https://grafana.com",
                    "description": "开源监控仪表板"
                },
                {
                    "name": "Kibana",
                    "url": "https://www.elastic.co/kibana",
                    "description": "Elasticsearch 可视化工具"
                },
                {
                    "name": "Prometheus",
                    "url": "https://prometheus.io",
                    "description": "开源监控系统"
                },
                {
                    "name": "Sentry",
                    "url": "https://sentry.io",
                    "description": "错误跟踪和性能监控"
                },
                {
                    "name": "DataDog",
                    "url": "https://www.datadoghq.com",
                    "description": "云端监控和分析平台"
                },
                {
                    "name": "New Relic",
                    "url": "https://newrelic.com",
                    "description": "应用性能监控"
                }
            ],
            "云服务": [
                {
                    "name": "AWS Console",
                    "url": "https://console.aws.amazon.com",
                    "description": "Amazon Web Services 控制台"
                },
                {
                    "name": "Google Cloud",
                    "url": "https://console.cloud.google.com",
                    "description": "Google Cloud Platform"
                },
                {
                    "name": "Azure Portal",
                    "url": "https://portal.azure.com",
                    "description": "Microsoft Azure 管理门户"
                },
                {
                    "name": "Heroku",
                    "url": "https://dashboard.heroku.com",
                    "description": "云应用部署平台"
                },
                {
                    "name": "Vercel",
                    "url": "https://vercel.com/dashboard",
                    "description": "前端部署平台"
                },
                {
                    "name": "Netlify",
                    "url": "https://app.netlify.com",
                    "description": "静态网站托管"
                }
            ],
            "设计工具": [
                {
                    "name": "Figma",
                    "url": "https://www.figma.com",
                    "description": "协作式界面设计工具"
                },
                {
                    "name": "Sketch",
                    "url": "https://www.sketch.com",
                    "description": "专业UI设计软件"
                },
                {
                    "name": "Adobe XD",
                    "url": "https://www.adobe.com/products/xd.html",
                    "description": "体验设计工具"
                },
                {
                    "name": "Zeplin",
                    "url": "https://zeplin.io",
                    "description": "设计交付平台"
                },
                {
                    "name": "InVision",
                    "url": "https://www.invisionapp.com",
                    "description": "数字产品设计平台"
                },
                {
                    "name": "Miro",
                    "url": "https://miro.com",
                    "description": "在线协作白板"
                }
            ],
            "沟通协作": [
                {
                    "name": "Slack",
                    "url": "https://slack.com",
                    "description": "团队沟通协作平台"
                },
                {
                    "name": "Microsoft Teams",
                    "url": "https://teams.microsoft.com",
                    "description": "微软团队协作工具"
                },
                {
                    "name": "Discord",
                    "url": "https://discord.com",
                    "description": "开发者社区平台"
                },
                {
                    "name": "Zoom",
                    "url": "https://zoom.us",
                    "description": "视频会议工具"
                },
                {
                    "name": "Google Meet",
                    "url": "https://meet.google.com",
                    "description": "Google 视频会议"
                },
                {
                    "name": "Miro",
                    "url": "https://miro.com",
                    "description": "在线协作白板"
                }
            ]
        }
    },
    "产品部门": {
        "description": "产品规划、设计和用户体验管理工具集",
        "groups": {
            "需求管理": [
                {
                    "name": "Productboard",
                    "url": "https://www.productboard.com",
                    "description": "产品需求管理平台"
                },
                {
                    "name": "Aha!",
                    "url": "https://www.aha.io",
                    "description": "产品路线图和功能规划"
                },
                {
                    "name": "Pivotal Tracker",
                    "url": "https://www.pivotaltracker.com",
                    "description": "敏捷项目跟踪工具"
                },
                {
                    "name": "UserVoice",
                    "url": "https://www.uservoice.com",
                    "description": "用户反馈收集平台"
                },
                {
                    "name": "Canny",
                    "url": "https://canny.io",
                    "description": "产品反馈管理"
                },
                {
                    "name": "Feature Upvote",
                    "url": "https://featureupvote.com",
                    "description": "功能投票和反馈系统"
                }
            ],
            "用户研究": [
                {
                    "name": "UserTesting",
                    "url": "https://www.usertesting.com",
                    "description": "用户测试和反馈平台"
                },
                {
                    "name": "Hotjar",
                    "url": "https://www.hotjar.com",
                    "description": "用户行为分析工具"
                },
                {
                    "name": "Typeform",
                    "url": "https://www.typeform.com",
                    "description": "在线表单和调研工具"
                },
                {
                    "name": "SurveyMonkey",
                    "url": "https://www.surveymonkey.com",
                    "description": "专业调研和问卷平台"
                },
                {
                    "name": "Optimal Workshop",
                    "url": "https://www.optimalworkshop.com",
                    "description": "用户体验研究工具套件"
                },
                {
                    "name": "Lookback",
                    "url": "https://lookback.io",
                    "description": "用户访谈和测试平台"
                }
            ],
            "原型设计": [
                {
                    "name": "Figma",
                    "url": "https://www.figma.com",
                    "description": "协作式界面设计工具"
                },
                {
                    "name": "Sketch",
                    "url": "https://www.sketch.com",
                    "description": "专业UI设计软件"
                },
                {
                    "name": "Adobe XD",
                    "url": "https://www.adobe.com/products/xd.html",
                    "description": "体验设计工具"
                },
                {
                    "name": "InVision",
                    "url": "https://www.invisionapp.com",
                    "description": "数字产品设计平台"
                },
                {
                    "name": "Framer",
                    "url": "https://www.framer.com",
                    "description": "交互原型设计工具"
                },
                {
                    "name": "Principle",
                    "url": "https://principleformac.com",
                    "description": "动画原型设计工具"
                }
            ],
            "数据分析": [
                {
                    "name": "Amplitude",
                    "url": "https://amplitude.com",
                    "description": "产品分析和用户行为追踪"
                },
                {
                    "name": "Mixpanel",
                    "url": "https://mixpanel.com",
                    "description": "用户行为分析平台"
                },
                {
                    "name": "Google Analytics",
                    "url": "https://analytics.google.com",
                    "description": "网站流量分析工具"
                },
                {
                    "name": "Tableau",
                    "url": "https://www.tableau.com",
                    "description": "商业智能和数据可视化"
                },
                {
                    "name": "Power BI",
                    "url": "https://powerbi.microsoft.com",
                    "description": "微软商业智能工具"
                },
                {
                    "name": "Looker",
                    "url": "https://looker.com",
                    "description": "企业级数据分析平台"
                }
            ],
            "项目协作": [
                {
                    "name": "Asana",
                    "url": "https://asana.com",
                    "description": "团队协作和任务管理"
                },
                {
                    "name": "Monday.com",
                    "url": "https://monday.com",
                    "description": "工作操作系统"
                },
                {
                    "name": "Notion",
                    "url": "https://www.notion.so",
                    "description": "多功能工作空间"
                },
                {
                    "name": "Miro",
                    "url": "https://miro.com",
                    "description": "在线协作白板"
                },
                {
                    "name": "FigJam",
                    "url": "https://www.figma.com/figjam/",
                    "description": "Figma 协作白板"
                },
                {
                    "name": "Whimsical",
                    "url": "https://whimsical.com",
                    "description": "流程图和思维导图工具"
                }
            ],
            "沟通工具": [
                {
                    "name": "Slack",
                    "url": "https://slack.com",
                    "description": "团队沟通协作平台"
                },
                {
                    "name": "Microsoft Teams",
                    "url": "https://teams.microsoft.com",
                    "description": "微软团队协作工具"
                },
                {
                    "name": "Zoom",
                    "url": "https://zoom.us",
                    "description": "视频会议工具"
                },
                {
                    "name": "Loom",
                    "url": "https://www.loom.com",
                    "description": "异步视频通信工具"
                },
                {
                    "name": "Gather",
                    "url": "https://gather.town",
                    "description": "虚拟办公室平台"
                },
                {
                    "name": "Discord",
                    "url": "https://discord.com",
                    "description": "社区协作平台"
                }
            ]
        }
    },
    "运营部门": {
        "description": "运营数据分析、用户增长和营销工具集",
        "groups": {
            "数据分析": [
                {
                    "name": "Google Analytics",
                    "url": "https://analytics.google.com",
                    "description": "网站流量分析工具"
                },
                {
                    "name": "Amplitude",
                    "url": "https://amplitude.com",
                    "description": "产品分析和用户行为追踪"
                },
                {
                    "name": "Mixpanel",
                    "url": "https://mixpanel.com",
                    "description": "用户行为分析平台"
                },
                {
                    "name": "GrowingIO",
                    "url": "https://www.growingio.com",
                    "description": "国内用户行为分析平台"
                },
                {
                    "name": "诸葛io",
                    "url": "https://zhugeio.com",
                    "description": "全域数据分析平台"
                },
                {
                    "name": "友盟+",
                    "url": "https://www.umeng.com",
                    "description": "移动应用数据统计平台"
                }
            ],
            "用户运营": [
                {
                    "name": "Intercom",
                    "url": "https://www.intercom.com",
                    "description": "客户沟通和支持平台"
                },
                {
                    "name": "Zendesk",
                    "url": "https://www.zendesk.com",
                    "description": "客户服务和支持平台"
                },
                {
                    "name": "Freshdesk",
                    "url": "https://freshdesk.com",
                    "description": "云端客服平台"
                },
                {
                    "name": "HubSpot",
                    "url": "https://www.hubspot.com",
                    "description": "CRM 和营销自动化平台"
                },
                {
                    "name": "Salesforce",
                    "url": "https://www.salesforce.com",
                    "description": "企业级 CRM 系统"
                },
                {
                    "name": "Pipedrive",
                    "url": "https://www.pipedrive.com",
                    "description": "销售 CRM 工具"
                }
            ],
            "内容营销": [
                {
                    "name": "Buffer",
                    "url": "https://buffer.com",
                    "description": "社交媒体管理和发布平台"
                },
                {
                    "name": "Hootsuite",
                    "url": "https://www.hootsuite.com",
                    "description": "社交媒体管理仪表板"
                },
                {
                    "name": "Later",
                    "url": "https://later.com",
                    "description": "Instagram 内容规划工具"
                },
                {
                    "name": "Canva",
                    "url": "https://www.canva.com",
                    "description": "在线设计和图形编辑工具"
                },
                {
                    "name": "Unsplash",
                    "url": "https://unsplash.com",
                    "description": "免费高质量图片资源库"
                },
                {
                    "name": "Pexels",
                    "url": "https://www.pexels.com",
                    "description": "免费图片和视频素材库"
                }
            ],
            "SEO工具": [
                {
                    "name": "Google Search Console",
                    "url": "https://search.google.com/search-console",
                    "description": "Google 网站搜索优化工具"
                },
                {
                    "name": "Ahrefs",
                    "url": "https://ahrefs.com",
                    "description": "SEO 分析和反向链接检查工具"
                },
                {
                    "name": "SEMrush",
                    "url": "https://www.semrush.com",
                    "description": "数字营销和SEO工具套件"
                },
                {
                    "name": "Moz",
                    "url": "https://moz.com",
                    "description": "SEO 和网站排名分析工具"
                },
                {
                    "name": "Screaming Frog",
                    "url": "https://www.screamingfrog.co.uk/seo-spider/",
                    "description": "网站爬虫和SEO分析工具"
                },
                {
                    "name": "GTmetrix",
                    "url": "https://gtmetrix.com",
                    "description": "网站性能和速度测试工具"
                }
            ],
            "广告投放": [
                {
                    "name": "Google Ads",
                    "url": "https://ads.google.com",
                    "description": "Google 广告投放平台"
                },
                {
                    "name": "Facebook Ads Manager",
                    "url": "https://www.facebook.com/adsmanager",
                    "description": "Facebook 广告管理平台"
                },
                {
                    "name": "TikTok Ads",
                    "url": "https://ads.tiktok.com",
                    "description": "TikTok 广告投放平台"
                },
                {
                    "name": "百度推广",
                    "url": "https://e.baidu.com",
                    "description": "百度搜索引擎广告平台"
                },
                {
                    "name": "巨量引擎",
                    "url": "https://www.oceanengine.com",
                    "description": "字节跳动广告投放平台"
                },
                {
                    "name": "腾讯广告",
                    "url": "https://e.qq.com",
                    "description": "腾讯广告投放平台"
                }
            ],
            "邮件营销": [
                {
                    "name": "Mailchimp",
                    "url": "https://mailchimp.com",
                    "description": "邮件营销和自动化平台"
                },
                {
                    "name": "Sendinblue",
                    "url": "https://www.sendinblue.com",
                    "description": "邮件营销和SMS平台"
                },
                {
                    "name": "ActiveCampaign",
                    "url": "https://www.activecampaign.com",
                    "description": "营销自动化和CRM平台"
                },
                {
                    "name": "ConvertKit",
                    "url": "https://convertkit.com",
                    "description": "创作者邮件营销平台"
                },
                {
                    "name": "Klaviyo",
                    "url": "https://www.klaviyo.com",
                    "description": "电商邮件营销平台"
                },
                {
                    "name": "Drip",
                    "url": "https://www.drip.com",
                    "description": "电商自动化营销平台"
                }
            ]
        }
    },
    "市场部门": {
        "description": "品牌建设、市场推广和竞争分析工具集",
        "groups": {
            "品牌设计": [
                {
                    "name": "Canva",
                    "url": "https://www.canva.com",
                    "description": "在线设计和图形编辑工具"
                },
                {
                    "name": "Adobe Creative Cloud",
                    "url": "https://www.adobe.com/creativecloud.html",
                    "description": "Adobe 创意设计工具套件"
                },
                {
                    "name": "Brandmark",
                    "url": "https://brandmark.io",
                    "description": "AI 品牌标志生成工具"
                },
                {
                    "name": "Looka",
                    "url": "https://looka.com",
                    "description": "AI 品牌设计生成器"
                },
                {
                    "name": "Hatchful by Shopify",
                    "url": "https://hatchful.shopify.com",
                    "description": "Shopify 品牌设计工具"
                },
                {
                    "name": "Coolors",
                    "url": "https://coolors.co",
                    "description": "配色方案生成工具"
                }
            ],
            "市场调研": [
                {
                    "name": "SurveyMonkey",
                    "url": "https://www.surveymonkey.com",
                    "description": "专业调研和问卷平台"
                },
                {
                    "name": "Typeform",
                    "url": "https://www.typeform.com",
                    "description": "在线表单和调研工具"
                },
                {
                    "name": "Qualtrics",
                    "url": "https://www.qualtrics.com",
                    "description": "企业级市场调研平台"
                },
                {
                    "name": "SurveyGizmo",
                    "url": "https://www.surveygizmo.com",
                    "description": "高级调研和表单工具"
                },
                {
                    "name": "Alchemer",
                    "url": "https://www.alchemer.com",
                    "description": "体验管理和调研平台"
                },
                {
                    "name": "QuestionPro",
                    "url": "https://www.questionpro.com",
                    "description": "在线调研和反馈平台"
                }
            ],
            "竞争分析": [
                {
                    "name": "SEMrush",
                    "url": "https://www.semrush.com",
                    "description": "数字营销和SEO工具套件"
                },
                {
                    "name": "Ahrefs",
                    "url": "https://ahrefs.com",
                    "description": "SEO 分析和反向链接检查工具"
                },
                {
                    "name": "SimilarWeb",
                    "url": "https://www.similarweb.com",
                    "description": "网站流量和竞争分析工具"
                },
                {
                    "name": "Alexa",
                    "url": "https://www.alexa.com",
                    "description": "网站排名和流量分析"
                },
                {
                    "name": "BuiltWith",
                    "url": "https://builtwith.com",
                    "description": "网站技术栈分析工具"
                },
                {
                    "name": "Crunchbase",
                    "url": "https://crunchbase.com",
                    "description": "创业公司和投资数据库"
                }
            ],
            "内容创作": [
                {
                    "name": "Grammarly",
                    "url": "https://www.grammarly.com",
                    "description": "AI 写作助手和语法检查工具"
                },
                {
                    "name": "Jasper",
                    "url": "https://www.jasper.ai",
                    "description": "AI 内容创作助手"
                },
                {
                    "name": "Copy.ai",
                    "url": "https://www.copy.ai",
                    "description": "AI 文案生成工具"
                },
                {
                    "name": "Writesonic",
                    "url": "https://writesonic.com",
                    "description": "AI 营销文案生成器"
                },
                {
                    "name": "Surfer SEO",
                    "url": "https://surferseo.com",
                    "description": "SEO 内容优化工具"
                },
                {
                    "name": "Hemingway",
                    "url": "http://www.hemingwayapp.com",
                    "description": "写作清晰度分析工具"
                }
            ],
            "社交媒体": [
                {
                    "name": "Buffer",
                    "url": "https://buffer.com",
                    "description": "社交媒体管理和发布平台"
                },
                {
                    "name": "Hootsuite",
                    "url": "https://www.hootsuite.com",
                    "description": "社交媒体管理仪表板"
                },
                {
                    "name": "Sprout Social",
                    "url": "https://sproutsocial.com",
                    "description": "社交媒体管理和分析平台"
                },
                {
                    "name": "Later",
                    "url": "https://later.com",
                    "description": "Instagram 内容规划工具"
                },
                {
                    "name": "TweetDeck",
                    "url": "https://tweetdeck.twitter.com",
                    "description": "Twitter 高级管理工具"
                },
                {
                    "name": "Crowdfire",
                    "url": "https://www.crowdfireapp.com",
                    "description": "社交媒体增长和分析工具"
                }
            ],
            "PR公关": [
                {
                    "name": "Meltwater",
                    "url": "https://www.meltwater.com",
                    "description": "媒体监测和品牌分析平台"
                },
                {
                    "name": "Cision",
                    "url": "https://www.cision.com",
                    "description": "PR 和媒体关系管理平台"
                },
                {
                    "name": "Brandwatch",
                    "url": "https://www.brandwatch.com",
                    "description": "社交媒体监听和品牌分析"
                },
                {
                    "name": "Mention",
                    "url": "https://mention.com",
                    "description": "品牌提及监测工具"
                },
                {
                    "name": "Google Alerts",
                    "url": "https://www.google.com/alerts",
                    "description": "Google 内容更新提醒服务"
                },
                {
                    "name": "Talkwalker",
                    "url": "https://www.talkwalker.com",
                    "description": "社交媒体和新闻监测平台"
                }
            ]
        }
    },
    "人力资源": {
        "description": "招聘管理、员工发展和组织发展工具集",
        "groups": {
            "招聘管理": [
                {
                    "name": "LinkedIn Recruiter",
                    "url": "https://recruiter.linkedin.com",
                    "description": "LinkedIn 招聘工具"
                },
                {
                    "name": "Greenhouse",
                    "url": "https://www.greenhouse.io",
                    "description": "招聘和人才管理平台"
                },
                {
                    "name": "Workday",
                    "url": "https://www.workday.com",
                    "description": "人力资源管理平台"
                },
                {
                    "name": "BambooHR",
                    "url": "https://www.bamboohr.com",
                    "description": "人力资源信息系统"
                },
                {
                    "name": "Indeed",
                    "url": "https://www.indeed.com/hire",
                    "description": "招聘广告和人才搜索平台"
                },
                {
                    "name": "Glassdoor",
                    "url": "https://www.glassdoor.com/employers",
                    "description": "雇主品牌和招聘平台"
                }
            ],
            "绩效管理": [
                {
                    "name": "15Five",
                    "url": "https://www.15five.com",
                    "description": "持续绩效管理和反馈平台"
                },
                {
                    "name": "Lattice",
                    "url": "https://lattice.com",
                    "description": "员工发展和管理平台"
                },
                {
                    "name": "Culture Amp",
                    "url": "https://www.cultureamp.com",
                    "description": "员工体验和绩效管理"
                },
                {
                    "name": "Workday Performance",
                    "url": "https://www.workday.com/en-us/products/performance-management.html",
                    "description": "Workday 绩效管理系统"
                },
                {
                    "name": "ADP Workforce Now",
                    "url": "https://www.adp.com",
                    "description": "人力资源和薪资管理平台"
                },
                {
                    "name": "SAP SuccessFactors",
                    "url": "https://www.sap.com/products/hcm.html",
                    "description": "SAP 人力资源管理套件"
                }
            ],
            "学习发展": [
                {
                    "name": "Coursera for Business",
                    "url": "https://www.coursera.org/business",
                    "description": "企业在线学习平台"
                },
                {
                    "name": "Udemy for Business",
                    "url": "https://business.udemy.com",
                    "description": "企业在线培训平台"
                },
                {
                    "name": "LinkedIn Learning",
                    "url": "https://learning.linkedin.com",
                    "description": "职业技能学习平台"
                },
                {
                    "name": "Degreed",
                    "url": "https://www.degrees.com",
                    "description": "终身学习和技能发展平台"
                },
                {
                    "name": "Skillsoft",
                    "url": "https://www.skillsoft.com",
                    "description": "企业培训和学习管理"
                },
                {
                    "name": "Moodle",
                    "url": "https://moodle.org",
                    "description": "开源学习管理系统"
                }
            ],
            "员工体验": [
                {
                    "name": "Officevibe",
                    "url": "https://www.officevibe.com",
                    "description": "员工敬业度和反馈平台"
                },
                {
                    "name": "Qualtrics EmployeeXM",
                    "url": "https://www.qualtrics.com/employee-experience",
                    "description": "员工体验管理平台"
                },
                {
                    "name": "Culture Amp",
                    "url": "https://www.cultureamp.com",
                    "description": "员工体验和绩效管理"
                },
                {
                    "name": "Glint",
                    "url": "https://www.glintinc.com",
                    "description": "员工反馈和洞察平台"
                },
                {
                    "name": "Peakon",
                    "url": "https://peakon.com",
                    "description": "员工体验和敬业度平台"
                },
                {
                    "name": "TINYpulse",
                    "url": "https://www.tinypulse.com",
                    "description": "员工反馈和认可平台"
                }
            ],
            "薪酬福利": [
                {
                    "name": "Paychex",
                    "url": "https://www.paychex.com",
                    "description": "薪资和人力资源服务"
                },
                {
                    "name": "Gusto",
                    "url": "https://gusto.com",
                    "description": "现代薪资和福利管理"
                },
                {
                    "name": "ADP",
                    "url": "https://www.adp.com",
                    "description": "人力资源和薪资管理"
                },
                {
                    "name": "TriNet",
                    "url": "https://www.trinet.com",
                    "description": "人力资源外包服务"
                },
                {
                    "name": "Namely",
                    "url": "https://www.namely.com",
                    "description": "HR 和薪资管理平台"
                },
                {
                    "name": "Zenefits",
                    "url": "https://www.zenefits.com",
                    "description": "人力资源和福利管理"
                }
            ],
            "组织发展": [
                {
                    "name": "Orgvue",
                    "url": "https://www.orgvue.com",
                    "description": "组织设计和人力规划平台"
                },
                {
                    "name": "Visier",
                    "url": "https://www.visier.com",
                    "description": "人力资本分析平台"
                },
                {
                    "name": "Workforce Software",
                    "url": "https://www.workforcesoftware.com",
                    "description": "劳动力管理和分析平台"
                },
                {
                    "name": "Tableau",
                    "url": "https://www.tableau.com",
                    "description": "人力资源数据可视化"
                },
                {
                    "name": "Power BI",
                    "url": "https://powerbi.microsoft.com",
                    "description": "人力资源分析仪表板"
                },
                {
                    "name": "Deloitte Greenhouse",
                    "url": "https://www2.deloitte.com/us/en/pages/consulting/solutions/deloitte-greenhouse.html",
                    "description": "组织发展和人才策略咨询"
                }
            ]
        }
    },
    "财务部门": {
        "description": "财务管理、预算控制和财务分析工具集",
        "groups": {
            "财务管理": [
                {
                    "name": "QuickBooks",
                    "url": "https://quickbooks.intuit.com",
                    "description": "中小企业财务管理软件"
                },
                {
                    "name": "Xero",
                    "url": "https://www.xero.com",
                    "description": "云端会计和财务管理"
                },
                {
                    "name": "FreshBooks",
                    "url": "https://www.freshbooks.com",
                    "description": "会计和发票管理工具"
                },
                {
                    "name": "Bench Accounting",
                    "url": "https://bench.co",
                    "description": "会计和财务报告服务"
                },
                {
                    "name": "Pilot",
                    "url": "https://pilot.com",
                    "description": "初创企业财务管理"
                },
                {
                    "name": "Brex",
                    "url": "https://brex.com",
                    "description": "企业信用卡和支出管理"
                }
            ],
            "预算规划": [
                {
                    "name": "Adaptive Insights",
                    "url": "https://www.adaptiveinsights.com",
                    "description": "企业绩效管理平台"
                },
                {
                    "name": "Anaplan",
                    "url": "https://www.anaplan.com",
                    "description": "企业规划和预算平台"
                },
                {
                    "name": "Host Analytics",
                    "url": "https://www.hostanalytics.com",
                    "description": "财务规划和分析平台"
                },
                {
                    "name": "Prophix",
                    "url": "https://www.prophix.com",
                    "description": "财务规划和预算管理"
                },
                {
                    "name": "Vena Solutions",
                    "url": "https://venasolutions.com",
                    "description": "财务规划和分析工具"
                },
                {
                    "name": "CCH Tagetik",
                    "url": "https://www.cch.com/software/tagetik",
                    "description": "企业绩效管理软件"
                }
            ],
            "财务分析": [
                {
                    "name": "Tableau",
                    "url": "https://www.tableau.com",
                    "description": "商业智能和数据可视化"
                },
                {
                    "name": "Power BI",
                    "url": "https://powerbi.microsoft.com",
                    "description": "微软商业智能工具"
                },
                {
                    "name": "Looker",
                    "url": "https://looker.com",
                    "description": "企业级数据分析平台"
                },
                {
                    "name": "ThoughtSpot",
                    "url": "https://www.thoughtspot.com",
                    "description": "AI 驱动的商业智能"
                },
                {
                    "name": "Sisense",
                    "url": "https://www.sisense.com",
                    "description": "商业智能和分析平台"
                },
                {
                    "name": "Domo",
                    "url": "https://www.domo.com",
                    "description": "商业智能和仪表板平台"
                }
            ],
            "税务合规": [
                {
                    "name": "TurboTax Business",
                    "url": "https://turbotax.intuit.com/business",
                    "description": "企业税务申报软件"
                },
                {
                    "name": "Bench Accounting",
                    "url": "https://bench.co",
                    "description": "会计和税务服务"
                },
                {
                    "name": "Brex",
                    "url": "https://brex.com",
                    "description": "企业支出和税务管理"
                },
                {
                    "name": "Pilot",
                    "url": "https://pilot.com",
                    "description": "初创企业税务和会计"
                },
                {
                    "name": "Botkeeper",
                    "url": "https://botkeeper.com",
                    "description": "自动化会计和税务服务"
                },
                {
                    "name": "ScaleFactor",
                    "url": "https://scalefactor.com",
                    "description": "中小企业会计服务"
                }
            ],
            "费用报销": [
                {
                    "name": "Expensify",
                    "url": "https://www.expensify.com",
                    "description": "费用报销和发票管理"
                },
                {
                    "name": "Zeni Finance",
                    "url": "https://www.zenifinance.com",
                    "description": "企业财务管理和报销"
                },
                {
                    "name": "Brex",
                    "url": "https://brex.com",
                    "description": "企业信用卡和支出跟踪"
                },
                {
                    "name": "Divvy",
                    "url": "https://www.divvy.com",
                    "description": "企业支出管理平台"
                },
                {
                    "name": "Spendesk",
                    "url": "https://www.spendesk.com",
                    "description": "企业支出和预算管理"
                },
                {
                    "name": "Nexonia",
                    "url": "https://www.nexonia.com",
                    "description": "费用报销和发票处理"
                }
            ],
            "审计风控": [
                {
                    "name": "MSCI RiskManager",
                    "url": "https://www.msci.com/riskmanager",
                    "description": "风险管理和合规平台"
                },
                {
                    "name": "RSA Archer",
                    "url": "https://www.rsa.com/en-us/products/information-risk-management/rsa-archer",
                    "description": "企业风险管理平台"
                },
                {
                    "name": "MetricStream",
                    "url": "https://www.metricstream.com",
                    "description": "合规管理和风险平台"
                },
                {
                    "name": "LogicGate",
                    "url": "https://www.logicgate.com",
                    "description": "风险和合规管理平台"
                },
                {
                    "name": "OneTrust",
                    "url": "https://www.onetrust.com",
                    "description": "隐私和数据治理平台"
                },
                {
                    "name": "NAVEX Global",
                    "url": "https://www.navexglobal.com",
                    "description": "道德和合规管理平台"
                }
            ]
        }
    }
}

def seed_demo_data():
    """生成演示数据"""
    from app import app, db
    with app.app_context():
        print("🌱 开始生成 WorkApp 多部门演示数据...")

        # 检查是否已有演示数据
        existing_workbenches = Workbench.query.filter(Workbench.name.in_([dept for dept in DEPARTMENTS.keys()])).all()
        if existing_workbenches:
            print("⚠️  演示数据已存在，跳过生成")
            return

        # 创建演示用户（如果不存在）
        demo_user = User.query.filter_by(userid='demo_user').first()
        if not demo_user:
            demo_user = User(
                userid='demo_user',
                name='企业管理员',
                avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=admin'
            )
            db.session.add(demo_user)
            db.session.commit()
            print("👤 创建演示用户")

        total_workbenches = 0
        total_groups = 0
        total_apps = 0

        # 为每个部门创建工作台
        colors = ['blue', 'green', 'purple', 'red', 'yellow', 'indigo', 'pink', 'gray']

        for dept_name, dept_data in DEPARTMENTS.items():
            # 创建工作台
            workbench = Workbench(
                name=dept_name,
                description=dept_data['description'],
                owner=demo_user
            )
            db.session.add(workbench)
            db.session.commit()
            print(f"🏢 创建{dept_name}工作台")
            total_workbenches += 1

            # 为工作台创建分组和应用
            for group_name, apps in dept_data['groups'].items():
                # 创建分组
                workspace = Workspace(
                    name=group_name,
                    is_public=True,  # 演示数据设为公开
                    workbench=workbench
                )
                db.session.add(workspace)
                db.session.commit()
                print(f"  📁 创建分组: {group_name}")
                total_groups += 1

                # 为分组添加应用
                for app_data in apps:
                    app = AppIcon(
                        name=app_data['name'],
                        description=app_data['description'],
                        url=app_data['url'],
                        color=random.choice(colors),
                        workspace=workspace
                    )
                    db.session.add(app)

                print(f"     ✅ 添加 {len(apps)} 个应用")
                total_apps += len(apps)

        db.session.commit()
        print("\n🎉 多部门演示数据生成完成！")
        print("📊 数据统计:")
        print(f"   - 工作台: {total_workbenches} 个")
        print(f"   - 分组: {total_groups} 个")
        print(f"   - 应用: {total_apps} 个")
        print("\n🚀 现在可以访问 http://localhost:5001 查看演示数据")
        print("   在侧边栏切换不同的部门工作台，体验完整的应用管理功能！")

def clear_demo_data():
    """清除演示数据"""
    from app import app, db
    with app.app_context():
        print("🧹 清除演示数据...")

        # 删除所有应用
        AppIcon.query.delete()

        # 删除所有分组
        Workspace.query.delete()

        # 删除所有演示工作台
        dept_names = list(DEPARTMENTS.keys())
        Workbench.query.filter(Workbench.name.in_(dept_names)).delete()

        # 删除演示用户
        User.query.filter_by(userid='demo_user').delete()

        db.session.commit()
        print("✅ 演示数据已清除")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_demo_data()
    else:
        seed_demo_data()