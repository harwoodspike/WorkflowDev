# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, response
from rest_framework.decorators import action

from app.models import WorkflowWizard


# Create your views here.
class TestViewSet(viewsets.ViewSet):
    def list(self, request, **kwargs):
        return response.Response({
            'msg': 'This is a test response from django api'
        })


class WorkflowViewSet(viewsets.ViewSet):
    def list(self, request, **kwargs):
        return response.Response(WorkflowWizard.objects.values())

    @action(detail=True)
    def get_step(self, request, pk, step=1):
        data = {'success': False, 'msg': 'Workflow not found'}
        try:
            wf = WorkflowWizard.objects.get(id=pk, active=True)
        except WorkflowWizard.DoesNotExist:
            pass

        else:
            cur_step = int(step) - 1
            if (cur_step + 1 <= wf.steps.count()):
                wfs = wf.steps.filter(active=True)[cur_step]
                data = {
                    'workflow': wf.name,
                    'step_name': wfs.name,
                    'step_desc': wfs.description,
                    'step_fields': None,
                }

                if wfs.form:
                    field_list = []
                    for field in wfs.form.fields.filter(active=True):
                        field_list.append({
                            'label': field.name,
                            'name': field.name,
                            'value': '',
                            'type': field.field_type,
                            'required': field.required,
                        })
                    data['step_fields'] = field_list
        return response.Response(data)

    def save(self, request, *args, **kwargs):
        return response.Response({'success': True})


class AppCategoryViewSet(viewsets.ViewSet):
    def list(self, request, **kwargs):
        return response.Response({
            'myapps': [
                {
                    'name': 'QBO',
                    'desc': 'This is our accounting system',
                    'link': 'https://qbo.intuit.com',
                    'alert_text': '',
                    'is_public': True,
                    'is_platinum': False,
                    'has_login': False,
                    'link_target': '',
                    'sub_title': 'Accounting System',
                    'show_image': True,
                    'logosrc': 'https://logo.clearbit.com/qbo.intuit.com/?size=500',
                    'id': 1,
                    'new_tab': False,
                }
            ],
            'app_categories': [
                {
                    'name': 'Marketing & Selling',
                    'apps': [
                        {
                            'id': 2,
                            'name': 'Fran Promote',
                            'desc': 'Promote or advertise your franchise system. Allow the world to see what your franchise has to offer.',
                            'link': 'http://example.com',
                            'sub_title': 'YOUR PROFILE AT FRANBOX',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Pt_6DnyYGz.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 3,
                            'name': 'Fran Gauge',
                            'desc': 'Sell your franchises on autopilot via our step-by-step franchise sales process.  Design a Franchisee On-boarding process of your own.',
                            'link': 'http://example.com',
                            'sub_title': 'AUTOMATE FRANCHISE DEVELOPMENT',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Ga_C33Ww7O.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 4,
                            'name': 'Fran Marketing Plan',
                            'desc': 'Develop a marketing plan that will give you and your team clarity and confidence to master customer acquisition.',
                            'link': 'http://example.com',
                            'sub_title': 'MASTER MARKETING AT EVERY UNIT',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Mp_AoQZHBW.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 5,
                            'name': 'Fran Sales Analytics',
                            'desc': 'Measure every business metric including all marketing activity, in one place, without having to upload or input any data.',
                            'link': 'http://example.com',
                            'sub_title': 'MAKE MARKETING ACCOUNTABLE',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Sa_FrXXiee.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 6,
                            'name': 'Fran A.I.',
                            'desc': 'Develop a marketing approach driven by A.I. that delivers in-market leads to every location at scale, anywhere you want.',
                            'link': 'http://example.com',
                            'sub_title': 'UTILIZE A.I. TO DOMINATE YOUR MARKET',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Ai_Nb3AdcD.svg',
                            'is_public': True,
                            'is_platinum': True,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 7,
                            'name': 'Fran Leads',
                            'desc': 'This massive dataset of over 300 million records helps you determine in-market and relevant leads across any segment.',
                            'link': '',
                            'sub_title': 'TARGETED LEADS TO SELL FRANCHISES',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>

<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Le_1_1.svg"></div>
<h1>FRAN Leads&trade;</h1><br /><br />
<p>Develop a marketing approach driven by A.I. that delivers in-market leads to every location at scale, anywhere you want.</p><br /><br />
<p>Use A.I. To Drive The Following Initiatives:</p><br />
<ul>
<li>Capture of high-targeted leads at scale</li>
<li>Customer experience discovery and optimization</li>
<li>Product feature optimization</li>
<li>Customer segmentation discovery / optimization</li>
<li>Discovery of optimal marketing messaging</li>
<li>Discovery of influencers in your market</li>
<li>Pricing optimization strategies</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Le_1.svg',
                            'is_public': True,
                            'is_platinum': True,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 8,
                            'name': 'Uniform CRM',
                            'desc': 'Full scale and fully customizable CRM for marketing, sales, and customer support activity management.',
                            'link': '',
                            'sub_title': 'INTEGRATED MARKETING CRM',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Uniform_CRM_24x.png"></div>
<h1>Uniform CRM&trade;</h1><br /><br />
<p>Full scale and fully customizable CRM for marketing, sales, and customer support activity management.</p><br /><br />
<ul>
<li>Pipeline Management: manage your entire sales pipeline with a kanban style interface to see progress of every prospect.</li>
<li>Landing Pages: launch and manage integrated landing pages.</li>
<li>Email Automation: create and manage the automation related to communication to your list(s).</li>
<li>Advanced Analytics: integrated pages and processes means you have advanced analytics to see into what prospects are really clicking on and doing.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Uniform_CRM_24x.png',
                            'is_public': True,
                            'is_platinum': True,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 9,
                            'name': 'Fran Focus',
                            'desc': 'Stay on top of sales and marketing activities and see instant reports on sales activity management... (coming soon)',
                            'link': '',
                            'sub_title': 'SALES ACTIVITY MANAGEMENT',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>

<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Fc_2_eqP8ThS.svg"></div>
<h1>FRAN Focus&trade;</h1><br /><br />
<p>Stay on top of sales and marketing activities and see instant reports on where you and your units are at for sales activity management.</p><br /><br />
<ul>
<li>Built for franchisors who have a manual marketing and sales approach and for franchisees who hate doing the manual work of business development or selling.</li>
<li>See exactly what activities will lead to hitting your goals and where you are at on your goals and activities in real-time.</li>
<li>Get alerts and reminders when your activities have not been logged and when you get behind.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Fc_2_sacKYI9.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 10,
                            'name': 'Traffic CRM',
                            'desc': 'Manage customers and your retails promotions.  This retail-focused CRM will get foot traffic... (coming soon)',
                            'link': '',
                            'sub_title': 'RETAIL FRANCHISE CRM',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/CRM_QDnGSdL.svg"></div>
<h1>Traffic CRM&trade;</h1><br /><br />
<p>Manage customers and your retail promotions that way you like to do business.  This retail-focused CRM will get foot traffic.</p><br /><br />
<p>Sell more goods with greater speed via our franchise-specific retail-based CRM.</p><br /><br />
<ul>
<li>Accelerate marketing results with your own built for retail CRM.</li>
<li>Automate and integrate SMS, MMS, email broadcasts, voice broadcasts, and more.</li>
<li>This CRM is built for restaurants and retail businesses.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/CRM_QDnGSdL.svg',
                            'is_public': True,
                            'is_platinum': True,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        }
                    ],
                }, {
                    'name': 'People & H.R.',
                    'apps': [
                        {
                            'id': 11,
                            'name': 'FRAN Academy',
                            'desc': 'Learn franchising from the top experts in the industry on every area of business and franchising. Attend classes and test out on your own time.',
                            'link': 'http://example.com',
                            'sub_title': 'BECOME A GURU AT FRANCHISING',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Ac_fUazmtQ.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 12,
                            'name': 'Fran Jobs',
                            'desc': 'This module will help you hire employees and manage the turnover at your business faster.',
                            'link': 'http://example.com',
                            'sub_title': 'AUTOMATE RECRUITING TEAM MEMBERS',
                            'alert_text': 'This module will help you hire employees and manage the turnover at your business faster.',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Jb_fvdLeyb.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 13,
                            'name': 'Fran Hire',
                            'desc': 'Automate and store securely all employee-related documentation for better speed, less headache and higher level of compliance.',
                            'link': 'http://example.com',
                            'sub_title': 'AUTOMATE ON-BOARDING TEAM MEMBERS',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Hr_HecCWf8.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 14,
                            'name': 'Fran Train',
                            'desc': 'Training so that you can map your training process for new franchisees in order to ensure your franchisees know how to run their unit(s).',
                            'link': 'http://example.com',
                            'sub_title': 'AUTOMATE TRAINING TEAM MEMBERS',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Tr_ocemAiP.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 15,
                            'name': 'Fran Chart',
                            'desc': 'This org and roles chart visualizes what responsibilities you and others in the organization have - now roles are clear to all!',
                            'link': 'http://example.com',
                            'sub_title': 'YOUR ORG CHART & TEAM ROLES',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Ch_M2QaSef.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 16,
                            'name': 'Fran Eval',
                            'desc': 'Do employee evaluations and get reminded of when those evaluations are due on both the franchisor and franchisee side... (coming soon)',
                            'link': '',
                            'sub_title': 'EMPLOYEE EVALUATION AUTOMATION',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>

<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Ev_2_FOZnMad.svg"></div>
<h1>FRAN Eval&trade;</h1><br /><br />
<p>Do employee evaluations and get reminded of when those evaluations are due on both the franchisor and franchisee side.</p><br /><br />
<ul>
<li>Connect employee evaluations to your existing recruiting, hiring and training processes.</li>
<li>Conduct seamlessly employee evaluations based on the job description, role and position of the person.</li>
<li>Employee evaluations connect automatically to your org chart and happen without your initiating them.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Ev_2_UqPDw2h.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 17,
                            'name': 'Fran CFO',
                            'desc': 'Hire a CFO today to improve your company overnight through next-level consulting and financial help... (coming soon)',
                            'link': '',
                            'sub_title': 'PORTAL FOR FINDING A PART-TIME CFO',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/CFO_dFgQAc2.svg"></div>
<h1>FRAN CFO&trade;</h1><br /><br />
<p>Hire a CFO today to improve your company overnight through next-level consulting and financial help.</p><br /><br />
<ul>
<li>Find a part-time Chief Financial Officer for your business - get the help you need without having to make a hire and commit to large amounts of money.</li>
<li>Require that the CFO be certified in your industry, methods, your business etc.</li>
<li>Get "matched" to the right CFO with our proprietary CFO matching technology.</li>
<li>Your choice - you choose the CFO right for you and if you ever change your mind, there are others to choose from. You are never held hostage by one person.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/CFO_8JiEfRu.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 18,
                            'name': 'Fran CMO',
                            'desc': 'Hire a chief marketing officer (CMO) for your organization and make an impact on sales today... (coming soon)',
                            'link': '',
                            'sub_title': 'PORTAL FOR FINDING A PART-TIME CMO',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/CMO_P9DVCYd.svg"></div>
<h1>FRAN CMO.&trade;</h1><br /><br />
<p>Hire a chief marketing officer (CMO) for your organization. These part-time CMOs are ready to come into your organization and make an impact on sales today.</p><br /><br />
<ul>
<li>Find a part-time Chief Marketing Officer for your business - get the help you need without having to make a hire and commit to large amounts of money.</li>
<li>Require that the CMO be certified in your methods, your plan, the Franbox marketing equation etc.</li>
<li>Get "matched" to the right CMO with our proprietary matching technology.</li>
<li>Your choice - you choose the CMO right for you and if you ever change your mind, there are others to choose from.  Switch when it feels right for you.  Plenty of options means you are never held hostage by one person.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/CMO_h5Lb6SL.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 19,
                            'name': 'Fran Messenger',
                            'desc': 'Collaborate on a secure level with chosen groups in a private way with permissions to your group... (coming soon)',
                            'link': '',
                            'sub_title': 'ROBUST COMMUNICATION PLATFORM APP',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Me_RQ5XUjY.svg"></div>
<h1>FRAN Messenger&trade;</h1><br /><br />
<p>Collaborate on a secure level with chosen groups in a private way with strict permissions to your group. Try and mobile app too.</p><br /><br />
<ul>
<li>Create a culture of rock stars who "gel" together by enabling next-gen communication.</li>
<li>Facilitate transparency and vulnerability inside of a safe communication space.</li>
<li>All messages and groups have encryption enabled and store data hippa-compliant.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Me_OPk8Jok.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 20,
                            'name': 'FRAN Health Plan',
                            'desc': 'Nationwide benefits tailored to franchise businesses in all states. Includes health, dental, vision and other employee benefits. (coming Soon)',
                            'link': '',
                            'sub_title': 'NATIONAL BENEFITS PROGRAM',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Hp_2_ULGqMD1.svg"></div>
<h1>FRAN Health Plan&trade;</h1><br /><br />
<p>Nationwide benefits tailored to franchise businesses in all states. Includes health, dental, vision and other employee benefits. (coming Soon)</p><br /><br />
<ul>
<li>Leverage the power and costs of a nationwide coverage network.</li>
<li>Coverage for each employee benefit.</li>
<li>Life, retirement, health, dental, vision and more.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Hp_2_ULGqMD1.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        }
                    ],
                }, {
                    'name': 'Operations',
                    'apps': [
                        {
                            'id': 21,
                            'name': 'FRAN Custom Plan',
                            'desc': 'Develop a checklist or planning process and create a custom tool that will give you and your team clarity and confidence.',
                            'link': 'http://example.com',
                            'sub_title': 'CREATE YOUR OWN TOOL',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Pn_caD6bnF.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 22,
                            'name': 'FRAN Vendors',
                            'desc': 'Find a recommended vendor to help your franchise fill a need to achieve success.  Vendors are from every area of business and franchising.',
                            'link': 'http://example.com',
                            'sub_title': 'APPROVED VENDOR NETWORK',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Vn_vHwQOe7.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 23,
                            'name': 'FRAN Ideas',
                            'desc': 'Create a private forum for questions, support issues, customer service or otherwise across your franchise business.',
                            'link': 'http://example.com',
                            'sub_title': 'YOUR FRANCHISE FORUM FOR IDEAS',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Id_MtH6PxA.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 24,
                            'name': 'FRAN Drive',
                            'desc': 'Store all your files so that all staff members and contractors can access the files needed to run all departments in your businesses.',
                            'link': 'http://example.com',
                            'sub_title': 'MEDIA LIBRARY & DOCUMENT STORAGE',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Dr_12y5g3o.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 25,
                            'name': 'FRAN Purchase',
                            'desc': 'Manage purchase requests and order fulfillment to and from franchisees - increase response rates and communication about orders.',
                            'link': '',
                            'sub_title': 'PURCHASING SOFTWARE FOR INVENTORY',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Pr_SkfuXhV.svg"></div>
<h1>FRAN Purchase&trade;</h1><br /><br />
<p>Manage purchase requests and order fulfillment to and from franchisees - increase response rates and transparent communication about orders.</p><br /><br />
<ul>
<li>Enable ordering at scale and online from franchisees (when goods are to be purchased from corporate or approved vendors).</li>
<li>Customize your payments and billing, shipping, labels, and more.</li>
<li>Completely automate orders with live inventory controls.</li>
<li>Enable unit owners to have their own retail shopping cart as well that connects to their live inventory.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Pr_PtCzqLG.svg',
                            'is_public': True,
                            'is_platinum': True,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 26,
                            'name': 'FRAN Tasks',
                            'desc': 'Manage your "to-do list" and tasks in this easy to use tool that helps you categorize tasks according to priority.',
                            'link': 'http://example.com',
                            'sub_title': 'SIMPLE TASK MANAGER AND NOTE TAKER',
                            'alert_text': 'Manage your "to-do list" and tasks in this easy to use tool that helps you categorize tasks according to priority.',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Tk_wCeEEcu.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 27,
                            'name': 'FRAN Units',
                            'desc': 'This information manager will help you keep track of each of your units and how to get in touch with them.',
                            'link': 'http://example.com',
                            'sub_title': 'UNIT OWNERSHIP DIRECTORY',
                            'alert_text': 'This information manager will help you keep track of each of your units and how to get in touch with them.',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Un_07a9v1A.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 28,
                            'name': 'FRAN Security',
                            'desc': 'Visualize all security threats in your business and mitigate cyber, physical, and administrative threats... (coming soon)',
                            'link': '',
                            'sub_title': 'BULLETPROOF YOUR COMPANY',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Sr_7zBjicX.svg"></div>
<h1>FRAN Security&trade;</h1><br /><br />
<p>Visualize all security threats in your business and mitigate cyber, physical, and administrative threats... (coming soon)</p><br /><br />
<ul>
<li>Cyber Threats: mitigate technical (cyber) security threats to each of your employees and your franchised unit employees.</li>
<li>Administrative Threats: mitigate admin security threats that could take your financial viability and ultimately take your company down.</li>
<li>Physical Threats: mitigate physical security threats that could take your assets, peace of mind and ability to operate.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Sr_V7jAZGg.svg',
                            'is_public': True,
                            'is_platinum': True,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 29,
                            'name': 'FRAN Comply',
                            'desc': 'Stay on top of compliance related to your industry and relationships with easy uploads, alerts, and simple verification... (coming soon)',
                            'link': '',
                            'sub_title': 'AUTOMATE AND MASTER COMPLIANCE',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Cp.svg"></div>
<h1>FRAN Comply&trade;</h1><br /><br />
<p>Stay on top of required compliance related to the industry and relationships with constituents with alerts and easy uploads... (coming soon).</p><br /><br />
<ul>
<li>Input every compliance document or project that needs attention, reminders or submissions to an authority.</li>
<li>Authorities receive documents validating your compliance seamlessly and without your manual submissions.</li>
<li>Alerts and reminders help you and your team(s) and unit(s) stay up on compliance matters year-round.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Cp_IrdBrYR.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 30,
                            'name': 'FRAN Hosting',
                            'desc': 'Host any website or web-based platform with one easy-to-use platform - all of your servers and websites in one secure place.',
                            'link': '',
                            'sub_title': 'SERVER & HOSTING PLATFORM',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Hosting.svg"></div>
<h1>FRAN Hosting&trade;</h1><br /><br />
<p>Host any website or web-based platform with one easy-to-use platform - all of your servers and websites in one secure place.</p><br /><br />
<ul>
<li>Sonar Monitoring:  sites and servers are monitored by sonar to determine the real-time availability or uptime of servers.</li>
<li>Cloud and Hybrid Server Network: whether your needs are dedicated servers, cloud servers or a hybrid solution, our network engineers can handle the setup, management and security of your server network.</li>
<li>Robust Hosting: manage all and any type of website platform using any language on our secure server network.  We currently manage hundreds of regular website platforms such as Wordpress, Drupal, Magento and others.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Hosting.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 31,
                            'name': 'Activated Sites',
                            'desc': 'Launch, activate and manage all your socially-enabled websites and landing pages in one easy to use system... (coming soon)',
                            'link': '',
                            'sub_title': 'WEBSITE & PAGE MANAGEMENT',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Sites.svg"></div>
<h1>Activated Sites&trade;</h1><br /><br />
<p>Launch, activate and manage all your socially-enabled websites and landing pages in one easy to use system... (coming soon)</p><br /><br />
<ul>
<li>Creation Tools: create and launch thousands of dollars in creative web design with clicks of a button.</li>
<li>Library of Designs: choose a design from our library and customize it your needs - get live in a flash.</li>
<li>Fully Hosted and Supported: easily manage your website through our portal with the security and easy of knowing we handle it all for you.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Sites.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        }
                    ],
                }, {
                    'name': 'Finance & Reporting',
                    'apps': [
                        {
                            'id': 32,
                            'name': 'FRAN Scoreboard',
                            'desc': 'Your accounting analysis tool that rides on top of your accounting system (QBO) to help you make the best decisions, easier.',
                            'link': 'http://example.com',
                            'sub_title': 'VISUALIZE FINANCIAL DATA AT SCALE',
                            'alert_text': '',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Sb_IeL8ebO.svg',
                            'is_public': True,
                            'is_platinum': True,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 33,
                            'name': 'FRAN Deals',
                            'desc': 'List your franchise business for sale here and get access to other franchise businesses for sale.',
                            'link': 'http://example.com',
                            'sub_title': 'FRANCHISE PURCHASES ON MARKET',
                            'alert_text': 'List your franchise business for sale here and get access to other franchise businesses for sale.',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Ds_SdVvmNx.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 34,
                            'name': 'FRAN Royalty',
                            'desc': 'Track royalty payments and automate royalty approvals with transparent reporting from franchisor to each franchisee.',
                            'link': 'http://example.com',
                            'sub_title': 'AUTOMATED ROYALTY REPORTING',
                            'alert_text': 'Track royalty payments and automate royalty approvals with transparent reporting from franchisor to each franchisee.',
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Ry_2_JZowzN4.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 35,
                            'name': 'FRAN Loans',
                            'desc': 'A network of lenders who can fund your business  - one simple applications leads you to the right lender for you... (coming soon)',
                            'link': '',
                            'sub_title': 'NETWORK OF FUNDING OPTIONS',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Ln_14x_eikoYNd.png"></div>
<h1>FRAN Loans&trade;</h1><br /><br />
<p>A network of lenders who can fund your business  - one simple application leads you to the right lender for you... (coming soon)</p><br /><br />
<ul>
<li>Credit Lines: credit lines are the most flexible, affordable and no-risk way to get your financial and funding model more robust really fast.  With such flexibility, every business should have access to multiple credit lines.  Whether you are in business a week or a decade, there are solutions here.</li>
<li>10-Year SBA Loans: these loans are quite affordable and are the easiest payment in the market, amortized over 10 years, they create cash within 90 days or so and are easily managed.</li>
<li>Equity Funding: venture debt, convertible notes, and other financing mechanisms can be a great way to get cash into your business quickly and painlessly.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Ln_14x_eikoYNd.png',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 36,
                            'name': 'FRAN Payment',
                            'desc': 'Make and take payments for royalties, tech fees, ad funds, and more via ACH... (coming soon)',
                            'link': '',
                            'sub_title': 'AUTOMATED PAYMENTS VIA ACH',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Py_25nutH3.svg"></div>
<h1>FRAN Payment&trade;</h1><br /><br />
<p>Make and take payments for royalties, tech fees, ad funds, and more via ACH... (coming soon).</p><br /><br />
<ul>
<li>Take and make royalty payments, ad fund payments, tech fee payments and any other type of payment from franchisor to franchisee automatically.</li>
<li>Connect FRAN Royalty to FRAN Payment for maximum effect.</li>
<li>All payments processed via ACH and are enabled for the fastest deposit time (2 days).</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Py_a9grJeI.svg',
                            'is_public': True,
                            'is_platinum': True,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 37,
                            'name': 'FRAN Scorekeeper',
                            'desc': 'Remove the manual work of bookkeeping and account and make your finances easy... (coming soon)',
                            'link': '',
                            'sub_title': 'AUTOMATE BOOKKEEPING / ACCOUNTING',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Sk_ZEmMCRb.svg"></div>
<h1>FRAN Scorekeeper&trade;</h1><br /><br />
<p>Remove the manual work of bookkeeping and account and make your finances easy... (coming soon)</p><br /><br />
<ul>
<li>Automate your bookkeeping: setup rules for how your A.I. engine codes your transactions before they ever hit your accounting system.</li>
<li>Connect to all of your financial accounts: use your new system to pull in data from every one of the accounts associated with your financial business life.</li>
<li>No more reconciliations: eliminate reconciliations and setup your automated bookkeeper / scorekeeper to pull transactions that may need your attention and alert you.</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Sk_PcdLi84.svg',
                            'is_public': True,
                            'is_platinum': True,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        },
                        {
                            'id': 38,
                            'name': 'FRAN Balance',
                            'desc': 'No need to log in to each bank account separately, simplify your process and view them all readily available on one platform. (coming soon)',
                            'link': '',
                            'sub_title': 'BANK BALANCES SNAPSHOT',
                            'alert_text': """<head>
<style>
h1 {color: black; text-align:center;}
ul {list-style-type: square; margin-left:30px;}
p,li {font-size:16px;}
img {margin-left: auto; margin-right: auto;}
</style>
</head>
<div style="text-align:center;"><img style="margin:10px" width="130" src="https://app.franbox.com/media/dashboard-images/Ba4x.png"></div>
<h1>FRAN Balance&trade;</h1><br /><br />
<p>No need to log in to each bank account separately, simplify your process and view them all readily available on one platform. (coming soon)</p><br /><br />
<ul>
<li>See all of your bank account balances in one place.</li>
<li>No need to log in to each bank account separately to see activity and balances</li>
<li>Works with virtually all US banking instructions</li>
</ul>
<div style="margin-bottom:30px;">&nbsp;</div>""",
                            'link_target': '',
                            'logosrc': 'https://app.franbox.com/media/dashboard-images/Ba_2_dx3sdTY.svg',
                            'is_public': True,
                            'is_platinum': False,
                            'has_login': False,
                            'show_image': True,
                            'new_tab': False,
                        }
                    ],
                }
            ],
        })
