import csv
import re
from datetime import datetime, timedelta
from time import sleep
from classes.send_sms_email import SendAMessage

class Logger():

    # Namespace(Action='log', 
    # print=False, search_end=None, 
    # search_start='2021-07-11')

    def __init__(self,config):
        self.config = config
        self.dag_log_list = []
        self.log_msg = ""
        self.csv_path_file = None


    def process_request(self):
        current_date = self.config.log_start

        f = open(self.config.dag_log_file, "r")
        lines = f.readlines()

        while True:
            found_dag = None
            for line in lines:
                if current_date in line:
                    found_dag = line
            self.dag_log_list.append(found_dag)

            current_date = datetime.strptime(current_date,"%Y-%m-%d")
            current_date = current_date + timedelta(days=1)
            current_date = datetime.strftime(current_date, "%Y-%m-%d")

            if not self.config.log_end or current_date >= self.config.log_end:
                break

        self.format_results()
        self.send_results()


    def format_results(self):
        # clean data
        self.dag_log_list = [x for x in self.dag_log_list if x != None]

        if not self.dag_log_list:
            self.log_msg = "No results Found...\n"
            self.log_msg += "Make sure format is correct:  YYYY-MM-DD\n"
            self.log_msg += "Example) 2021-07-03"
        else:
            if self.config.csv:
                self.setup_csv()
            for line in self.dag_log_list:
                line = line.split("|")
                if self.config.csv:
                    data_line = []
                    for n in range(0,len(line)):
                        if n != 0: # date
                            line[n] = re.sub('[^0-9,.]','',line[n])
                        data_line.append(line[n])
                    self.data.append(data_line)
                self.log_msg += f"Date: {line[0]}\n"
                self.log_msg += f"DAG WALLET AMT: {'{:,}'.format(int(line[1]))}\n"
                if len(line) > 2:  # legacy error check -- deprecate in next version               
                    self.log_msg += f"USD VALUE {'${:,.2f}'.format(float(line[2]))}\n"
                if len(line) > 3:  # legacy error check -- deprecate in next version
                    self.log_msg += f"DAG VALUE {'${:,.2f}'.format(float(line[3]))}\n"
                self.log_msg += "===\n"
    

    def send_results(self):
        if self.config.local:
            print("SEARCH RESULTS\n===")
            print(f"{self.log_msg}\n")

        if self.config.csv:
            with open(self.csv_path_file, 'w', encoding="UTF8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)
                writer.writerows(self.data)
        
        if not self.config.silence_email and not self.config.local:
            SendAMessage("normal",self.log_msg,self.config,self.csv_path_file)


    def setup_csv(self):
        self.header = ['date','dag_end_balance','usd_value','dag_in_usd']
        self.data = []

        file_name = f"{self.config.current_date}_search_{self.config.log_start}"
        if not self.config.log_end:
            file_name += f"_{self.config.log_end}"
        self.csv_path_file = f"{self.config.dag_log_file_path}{file_name}.csv"


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")
  