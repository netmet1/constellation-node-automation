import os
import re
from datetime import datetime, timedelta

class CreateReport():

    def __init__(self, report_type, usd_dag_price,config):
        self.config = config
        self.usd_dag_price = usd_dag_price
        self.report_type = report_type

        self.today = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M")
        # self.today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.report_str = ""
        self.dag_metrics = []
        self.usd_metrics = []
        self.dag_usd_dict = {}

        self.daily_report()


    def daily_report(self):
        counter = 0
        dags = 0
        usd = 0
        dag_dict = {}
        usd_dict = {}
        

        f = open(f"/{self.config.username}/automation/dag_count.log","r")
        lines = f.readlines()
        last_line = lines[len(lines)-1]

        first = True

        for line in lines:
            if self.today in line:
                parse_item = line.split("|")
                dags = int(parse_item[1])
                usd = float(parse_item[2])
                dag_usd_price = float(parse_item[3])

                if first:
                    first = False
                    dag_dict["first"] = dags
                    usd_dict["first"] = usd
                    self.dag_usd_dict["first"] = dag_usd_price
                if line == last_line:
                    dag_dict["last"] = dags
                    usd_dict["last"] = usd
                    self.dag_usd_dict["last"] = dag_usd_price

        print(dag_dict)
        print(usd_dict)
        print(self.dag_usd_dict)

        dags_for_day = dag_dict["last"] - dag_dict["first"]
        # usd_for_day = usd_dict["last"] - usd_dict["first"]
        dag_change = '{:.8f}'.format(self.dag_usd_dict["last"] - self.dag_usd_dict["first"])

        counters = [1, self.config.day_run_hours*4, self.config.day_run_hours*2, self.config.day_run_hours]
        estimators = [24,720,8640] # 1 day, 1 month, 1 year

        # counters = [1,52,26,13] # 13 hour day, 15min, 30min, 1hr
        self.config.report_estimates.insert(0,self.usd_dag_price)

        self.dag_metrics = [int(round((dags_for_day/x),0)) for x in counters]
        self.usd_metrics = [[round(((self.dag_metrics[3]*x)*y),2) for x in estimators] for y in self.config.report_estimates ]

        self.build_string(dag_change)

        cont_str = "" # declare
        for n,metric in enumerate(self.usd_metrics):
            cont_str += "========\n"
            cont_str += f"USD @ ${self.config.report_estimates[n]}\n"
            cont_str += f"DAILY   : ${metric[0]:,}\n"
            cont_str += f"MONTHLY : ${metric[1]:,}\n"
            cont_str += f"YEARLY  : ${metric[2]:,}\n"

        self.report_str += cont_str

    
    def build_string(self,dag_change):
        self.report_str = f"""
END OF DAY REPORT
=================
{self.config.day_time_frame} 
START: {self.config.current_date} {self.config.start_time}
END: {self.config.current_date} {self.config.end_time}
---
REWARDS: {self.dag_metrics[0]:,}
AVE/15Min: {self.dag_metrics[1]:,}
AVE/30Min: {self.dag_metrics[2]:,}
AVE/1Hour: {self.dag_metrics[3]:,}
---
$DAG DAY START: {self.dag_usd_dict["first"]}
$DAG DAY END  : {self.dag_usd_dict["last"]}
$DAG CHANGE   : {dag_change}
---
$DAG ESTIMATES
Daily  : {self.dag_metrics[3]*24:,}
Monthly: {self.dag_metrics[3]*720:,}
Yearly : {self.dag_metrics[3]*8760:,}
"""


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")




