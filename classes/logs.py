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


    def process_request(self):
        self.verify_config()
        found_dag = None
        current_date = self.config.log_start

        f = open(self.config.dag_log_file, "r")
        lines = f.readlines()

        while True:
            for line in lines:
                if current_date in line:
                    found_dag = line
            self.dag_log_list.append(found_dag)

            current_date = datetime.strptime(current_date,"%Y-%m-%d")
            current_date = current_date + timedelta(days=1)
            current_date = datetime.strftime(current_date, "%Y-%m-%d")

            if self.config.log_end is None or current_date >= self.config.log_end:
                break

        self.format_results()
        self.send_results()


    def format_results(self):
        if self.dag_log_list[0] is None:
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
                        data_line.append(re.sub('[^0-9,.]','',line[n]))
                    self.data.append(data_line)
                self.log_msg += f"Date: {line[0]}\n"
                self.log_msg += f"DAG WALLET AMT: {'{:,}'.format(int(line[1]))}\n"
                self.log_msg += f"USD VALUE {'${:,.2f}'.format(float(line[2]))}\n"
                self.log_msg += f"DAG VALUE {'${:,.2f}'.format(float(line[3]))}\n===\n"
    

    def send_results(self):
        email_type = "normal"

        if self.config.local:
            print("SEARCH RESULTS\n===")
            print(f"{self.log_msg}\n")

        if self.config.csv:
            with open(self.csv_path_file, 'w', encoding="UTF8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)
                writer.writerows(self.data)
            email_type = "csv"
        
        if not self.config.silence_email:
            SendAMessage(email_type,self.log_msg,self.config)


    def verify_config(self):
        self.test_date(self.config.log_start)
        if self.config.log_end is not None:
            self.test_date(self.config.log_end)


    def test_date(self,date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            print("Incorrect date format supplied\nPlease refer to the --help")
            print("python3 automation.py log --help\n\n")
            exit(1)


    def setup_csv(self):
        self.header = ['date','dag_accumulation','usd_value','dag_in_usd']
        self.data = []

        file_name = f"{self.config.current_date}_search_{self.config.log_start}"
        if self.config.log_end != None:
            file_name += f"_{self.config.log_end}"
        self.csv_path_file = f"{self.config.dag_log_file_path}{file_name}.csv"


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")
  