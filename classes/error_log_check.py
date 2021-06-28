import os
import sys
import time

class ErrorLogCheck():

    def __init__(self,config):
        self.config = config
        self.log_file_path = f"/{self.config.username}/constellation/logs/"
        self.log_file_name = "app.log"

        self.abs_log_file = self.log_file_path+self.log_file_name

        self.error_report_body = ""
        self.number_of_lines = 0
        self.error_count = 0
        self.percentage_errors = 0
        self.check_log_for_errors()

        self.percent = (self.error_count/self.number_of_lines)*100
        self.percent = round(self.percent,4)

        self.create_error_report_msg()


    def check_log_for_errors(self):
        with open(self.abs_log_file) as logger:
            log_lines = logger.readlines()
            self.number_of_lines = len(log_lines)
            for line in log_lines:
                if line.find("ERROR") > -1:
                    self.error_count = self.error_count + 1


    def create_error_report_msg(self):
        if self.error_count > self.config.error_max:
            self.error_report_body = f"""
Log Size: {self.number_of_lines}
Errors:: {self.error_count}
Percentage:: {self.percent}%
            """

if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")

    
