import csv
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


    def process_request(self):
        self.verify_config()
        dag_found = None
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

            if self.config.log_end is None or current_date > self.config.log_end:
                break

        self.format_results()


    def format_results(self):
        log_msg = ""
        for line in self.dag_log_list:
            line = line.split("|")
            log_msg += f"Date: {line[0]}\n"
            log_msg += f"DAG WALLET AMT: {'{:,}'.format(int(line[1]))}\n"
            log_msg += f"USD VALUE {'${:,.2f}'.format(float(line[2]))}\n"
            log_msg += f"DAG VALUE {'${:,.2f}'.format(float(line[3]))}\n===\n"
            
        SendAMessage("normal",log_msg,self.config)
    

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


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")
  