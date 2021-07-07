from datetime import datetime, timedelta
from time import sleep
from pprint import pprint

from classes.error_log_check import ErrorLogCheck 
from classes.check_dag_status import CheckDagStatus
from classes.send_sms_email import SendAMessage
from classes.reports import CreateReport
from classes.config_obj import Config

class Core():

    def __init__(self,config):
        self.config = config


    def node_checkup(self):

        checkForErrors = ErrorLogCheck(self.config)
        buildReport = CheckDagStatus(self.config)

        if checkForErrors.error_count > self.config.error_max:
            msg = checkForErrors.error_report_body+"\n\n"+buildReport.report_body
            msg_action = "error"
        else:
            msg = buildReport.report_body
            msg_action = "normal"

        if self.config.create_report is True:
            if self.config.report_enabled is True:
                createReport = CreateReport("daily", buildReport.usd_dag_price, self.config)
                msg = createReport.report_str 
            else:
                msg_action = "silent"

        if msg_action != "silent" and self.config.silence_email is False:
            SendAMessage(msg_action,msg,self.config)


    def auto_run_schedule(self):
        now = datetime.now().strftime("%H:%M")
        now = datetime.now().strptime(now,"%H:%M").time()

        # If the auto param is called, this loop will never be exited, until the job is
        # killed or the ctl-c. This program is designed to run continuously. 
        while True:
            if now >= self.config.start_time and now <= self.config.end_time: 
                while True:
                    if self.config.last_run == "never":
                        now = datetime.now().strftime("%H:%M")
                        now = datetime.now().strptime(now,"%H:%M").time()
                        if self.config.alert_interval > 60:
                            # lazy way out.
                            # if the interval is over 60 minutes, start on the quarter hour.
                            start_interval = 15
                        else:
                            start_interval = self.config.alert_interval

                        for n in range(0,60,start_interval):
                            if now.minute == n:
                                # set time first to avoid synchronous distortion
                                self.config.last_run = datetime.now()
                                self.node_checkup()
                                break

                        if self.config.last_run != "never":
                            break
                        sleep(2)
                    else:
                        break

                while True:
                    now = datetime.now().strftime("%H:%M")
                    now = datetime.now().strptime(now,"%H:%M").time()

                    next_run = self.config.last_run + timedelta(minutes=self.config.alert_interval)
                    next_run = next_run.strftime("%H:%M")
                    next_run = datetime.strptime(next_run,"%H:%M").time()
                    last_run = self.config.last_run.strftime("%H:%M")
                    last_run = datetime.strptime(last_run,"%H:%M").time()

                    if (now >= self.config.start_time and now <= self.config.report_time) and last_run < self.config.report_time: 
                        if now == self.config.report_time:
                            self.config.last_run = datetime.now()
                            self.config.create_report = True
                            self.config.silence_writelog = True
                            self.node_checkup()
                        elif now >= next_run:
                            self.config.last_run = datetime.now()
                            self.config.create_report = False
                            self.config.silence_writelog = False
                            self.node_checkup()

                            if self.config.reload_needed():
                                # rebuild configuration because user modified
                                self.config = Config(self.config.dag_args)
                                break
                        sleep(2)
                    else:
                        break
            else:
                # force config back to alert settings to avoid reload_needed loop
                self.config = Config(self.config.dag_args) 
                # reset the last_run for next day (time slots)
                self.config.last_run = "never"
                now = datetime.now().strftime("%H:%M")
                now = datetime.now().strptime(now,"%H:%M").time()
                sleep(2)


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")
