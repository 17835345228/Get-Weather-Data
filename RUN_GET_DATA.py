#!/usr/bin/python3
# -*- coding:utf-8 -*-
# project:
# user:哦！再见
# Author: _bggacyy
# createtime: 2020/10/15 15:31


import smtplib
from email.mime.text import MIMEText
from email.header import Header
from apscheduler.schedulers.blocking import BlockingScheduler
from Get_Day_Data import Project_One


"""
定时器
授权码：iiyvcbleqopvfgfg
"""


def send_email(str):
    my_addr = '1154622707@qq.com'
    password = 'iiyvcbleqopvfgfg'

    to_addr = '17835345228@163.com'
    to_addr2 = '2015711377@qq.com'

    smtp_server = "smtp.qq.com"

    msg = MIMEText(str, 'plain', 'utf-8')

    msg['From'] = Header(my_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('Log Message')
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(my_addr, password)
        server.sendmail(my_addr, [to_addr,to_addr2], msg.as_string())
        server.quit()
    except Exception as e:
        pass


if __name__ == '__main__':
    try:
        str = '数据获取成功'
        sched = BlockingScheduler()

        @sched.scheduled_job('cron', day_of_week='*', hour=19, minute='24')
        def job():
            get_data = Project_One()
            get_data.run()
            send_email(str)
        sched.start()
    except Exception as e:
        str1 = "数据获取失败"
        send_email(str1)
