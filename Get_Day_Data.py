#!/usr/bin/python3
# -*- coding:utf-8 -*-
# project:
# user:哦！再见
# Author: _bggacyy
# createtime: 2020/10/9 15:02

"""
    http://api.data.cma.cn:8090/api?userId=<帐号>&pwd=<密码>&dataFormat=json&
    interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR&
    timeRange=<时间范围>&staIDs=<台站列表>&elements=Station_Id_C,Year,Mon,Day,Hour,<要素列表>

   用户名:603010394275ngbP8
   密码:7xdrcEk

    {"returnCode":"0","returnMessage":"Query Succeed","rowCount":"8","colCount":"8",
    "requestParams":"datacode=SURF_CHN_MUL_HOR&staids=57586&timerange=[20201009000000,20201009230000]
    &elements=Station_Id_C,Year,Mon,Day,Hour,TEM,TEM_Max,TEM_Max",
    "requestTime":"2020-10-09 07:53:54","responseTime":"2020-10-09 07:53:54",
    "takeTime":"0.027","fieldNames":"区站号(字符) 年 月 日 时 温度/气温 最高气温 最高气温",
    "fieldUnits":"- 年 月 日 时 摄氏度(℃) 摄氏度(℃) 摄氏度(℃)",
    "DS":[{"Station_Id_C":"57586","Year":"2020","Mon":"10","Day":"9","Hour":"0","TEM":"15.9000","TEM_Max":"15.9000","TEM_Max":"15.9000"},
    {"Station_Id_C":"57586","Year":"2020","Mon":"10","Day":"9","Hour":"1","TEM":"17.9000","TEM_Max":"18.3000","TEM_Max":"18.3000"},
    {"Station_Id_C":"57586","Year":"2020","Mon":"10","Day":"9","Hour":"2","TEM":"21.0000","TEM_Max":"21.0000","TEM_Max":"21.0000"},
    {"Station_Id_C":"57586","Year":"2020","Mon":"10","Day":"9","Hour":"3","TEM":"22.7000","TEM_Max":"22.9000","TEM_Max":"22.9000"},
    {"Station_Id_C":"57586","Year":"2020","Mon":"10","Day":"9","Hour":"4","TEM":"24.3000","TEM_Max":"24.4000","TEM_Max":"24.4000"},
    {"Station_Id_C":"57586","Year":"2020","Mon":"10","Day":"9","Hour":"5","TEM":"24.5000","TEM_Max":"25.0000","TEM_Max":"25.0000"},
    {"Station_Id_C":"57586","Year":"2020","Mon":"10","Day":"9","Hour":"6","TEM":"25.1000","TEM_Max":"25.1000","TEM_Max":"25.1000"},
    {"Station_Id_C":"57586","Year":"2020","Mon":"10","Day":"9","Hour":"7","TEM":"23.9000","TEM_Max":"25.3000","TEM_Max":"25.3000"}]}

    我国共有34个省级行政区域，包括23个省，5个自治区，4个直辖市，2个特别行政区。

站台号,时间,气压,最高气压,最低气压,温度,最高气温,最低气温,相对湿度,最小相对湿度,降水量,最大风速,现在天气,体感温度
"""
import requests
import json
import xlrd
import csv
import time
import os.path
import logging


class Project_One:
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4270.0 Mobile Safari/537.36"}
        self.list_failure = []
        file_exist = os.path.isfile("2170_station_data.csv")
        if file_exist == True:
            pass
        else:
            f = open(
                "2170_station_data.csv",
                'a+',
                encoding='gbk',
                newline="")
            csv_writer = csv.writer(f)
            csv_writer.writerow(
                ["站台号", "年", "月", "日", "时间", "气压", "最高气压", "最低气压", "温度", "最高气温", "最低气温", "相对湿度", "最小相对湿度", "降水量",
                 "最大风速", "现在天气", "体感温度"])
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        log_name = 'Message.log'
        logfile = log_name
        fh = logging.FileHandler(logfile, mode='a+')
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)
    # 获取URL地址

    def get_url(self, st_id_index):
        mon_list = [1,3,5,7,8,10,12]
        t = time.localtime()
        year = str(time.strftime("%Y", t))
        mon = time.strftime("%m", t)
        day = str(int(time.strftime("%d", t)) - 1)
        if day == 1:
            mon = str(int(time.strftime("%m", t))-1)
            if (int(mon) in mon_list):
                day = str(31)
            else:
                day = str(30)
            if int(mon) == 2:
                if (int(year)%4==0) and (int(year)%100 != 0) or (int(year)%400==0):
                    day = str(29)
                else:
                    day = str(28)
        if (int(mon) ==1 and int(day) ==1):
            year = str(int(year)-1)
            mon = str(12)
            day = str(31)
        url = "http://api.data.cma.cn:8090/api" \
              "?userId=603010394275ngbP8&pwd=7xdrcEk" \
              "&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID" \
              "&dataCode=SURF_CHN_MUL_HOR&timeRange=[{0}{1}{2}000000,{0}{1}{2}230000]" \
              "&staIDs={3}" \
            "&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Max,PRS_Min,TEM,TEM_Max,TEM_Min,RHU,RHU_Min,PRE_1h,WIN_S_Max,WEP_Now,tigan".format(
                year, mon,day, st_id_index)
        return url

    # 获取区站号列表
    def station_list(self):
        file_path = 'China_SURF_Station.xlsx'
        data = xlrd.open_workbook(file_path)
        table = data.sheet_by_index(0)
        cols_values = table.col_values(0)
        return cols_values

    # 获取response对象

    def get_response(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            return response
        except Exception as e:
            # print("\033[31m获取请求失败...\033[0m")
            # print("\033[31m{}\033[0m".format(e))
            pass
    # 处理返回的json数据并且写入csv文件

    def dispose_json(self, response):
        list_Emlements = json.loads(response.content.decode())["DS"]
        list_len = len(list_Emlements)
        f = open('2170_station_data.csv', 'a+', encoding='gbk', newline="")
        csv_writer = csv.writer(f)
        for i in range(list_len):
            station_id = list_Emlements[i]["Station_Id_C"]
            hour = list_Emlements[i]["Hour"]
            YEAR = list_Emlements[i]["Year"]
            MON = list_Emlements[i]["Mon"]
            DAY = list_Emlements[i]["Day"]
            PRS = list_Emlements[i]["PRS"]
            PRS_MAX = list_Emlements[i]["PRS_Max"]
            PRS_MIN = list_Emlements[i]["PRS_Min"]
            TEM = list_Emlements[i]["TEM"]
            TEM_MAX = list_Emlements[i]["TEM_Max"]
            TEM_MIN = list_Emlements[i]["TEM_Min"]
            RHU = list_Emlements[i]["RHU"]
            RHU_MIN = list_Emlements[i]["RHU_Min"]
            PRE_1h = list_Emlements[i]["PRE_1h"]
            WIN_S_MAX = list_Emlements[i]["WIN_S_Max"]
            WEP_NOW = list_Emlements[i]["WEP_Now"]
            tigan = list_Emlements[i]["tigan"]
            csv_writer.writerow([station_id,
                                 YEAR,
                                 MON,
                                 DAY,
                                 hour,
                                 PRS,
                                 PRS_MAX,
                                 PRS_MIN,
                                 TEM,
                                 TEM_MAX,
                                 TEM_MIN,
                                 RHU,
                                 RHU_MIN,
                                 PRE_1h,
                                 WIN_S_MAX,
                                 WEP_NOW,
                                 tigan])
        

    def reget_url(self):
        Tag = 10
        while Tag > 0:
            if len(self.list_failure) == 0:
                # print("\033[32mALL SUCCEED\033[0m")
                break
            else:
                for j in self.list_failure:
                    index = str(int(j))
                    try:
                        # print("\033[33m站台{}获取数据中...\033[0m".format(index))
                        url = self.get_url(index)
                        r = self.get_response(url)
                        self.dispose_json(r)
                        self.list_failure.remove(j)
                        # print("\033[33m站台{}获取数据成功...\033[0m".format(index))
                    except Exception as e:
                        self.list_failure.append(j)
                        # print(
                        #     "\033[31m站台{}获取数据失败，错误为：{}\033[0m".format(
                        #         index, e))
                        time.sleep(1)
                        continue
            Tag = Tag - 1

    def run(self):
        station_id = self.station_list()
        station_id.remove("区站号")
        station_JD1 = station_id[-1]
        station_id.remove(station_JD1)
        station_JD2 = station_id[-1]
        station_id.remove(station_JD2)
        t = time.localtime()
        year = str(time.strftime("%Y", t))
        mon = time.strftime("%m", t)
        day = str(int(time.strftime("%d", t)) - 1)
        self.logger.info("抓取{}-{}-{}的数据".format(year, mon, day))

        for i in station_id:
            index = str(int(i))
            try:
                url = self.get_url(index)
                r = self.get_response(url)
                self.dispose_json(r)
                # print("\033[32m站台{}获取数据成功...\033[0m".format(index))
            except Exception as e:
                self.list_failure.append(i)
                # print("\033[31m站台{}获取数据失败，错误为：{}\033[0m".format(index, e))
                time.sleep(1)
                continue
        if len(self.list_failure) == 0:
            self.logger.info("数据全部获取成功")
        else:
            self.reget_url()


# if __name__ == '__main__':
#
#     try:
#         project_one = Project_One()
#         print("程序开始:{}".format(time.ctime()))
#         project_one.run()
#         print("It's OK")
#         print("程序结束:{}".format(time.ctime()))
#     except Exception as e:
#         print(e)
#         print("程序结束:{}".format(time.ctime()))
