import builtins
from datetime import datetime, timedelta
from time import sleep
from pprint import pprint

from classes.error_log_check import ErrorLogCheck 
from classes.check_dag_status import CheckDagStatus
from classes.send_sms_email import SendAMessage
from classes.reports import CreateReport
from classes.config_obj import Config
from classes.up_monitor import UpMonitor

class Core():

    def __init__(self,config):
        self.config = config
        self.msg = ""
        self.msg_action = ""

        # create session health check monitor obj
        self.up_monitor = UpMonitor(self.config)


    def node_checkup(self):
        self.config.health_failure = self.up_monitor.health_failure # set health state
        checkForErrors = ErrorLogCheck(self.config)
        buildReport = CheckDagStatus(self.config)

        if checkForErrors.error_count > self.config.error_max:
            self.msg = checkForErrors.error_report_body+"\n\n"+buildReport.report_body
            self.msg_action= "error"
        else:
            self.msg = buildReport.report_body
            self.msg_action= "normal"

        if self.config.create_report is True:
            if self.config.report_enabled is True:
                createReport = CreateReport("daily", buildReport, self.config)
                self.msg = createReport.report_str 
            else:
                self.msg_action= "silent"

        self.send_alert()

    
    def node_health(self,now=None):
        def check():
            self.up_monitor.perform_healthchecks()
            self.msg = self.up_monitor.build_health_msg()
            self.msg_action = self.config.action

        if self.config.action == "auto":
            if self.config.health_enabled and (now >= self.up_monitor.next_health_check or self.up_monitor.first_run):
                # no longer first time
                self.up_monitor.first_run = False
                # setup next run time
                self.up_monitor.next_health_check = self.config.build_time(
                    self.config.health_int,
                    "closest_forward"
                )  
                check()
                if self.up_monitor.health_failure:
                    if self.up_monitor.alarm_triggered and self.config.health_alarm_once:
                        return
                    else:
                        self.up_monitor.alarm_triggered = True
                else:
                    if self.up_monitor.alarm_triggered:
                        self.up_monitor.alarm_triggered = False
                    else:
                         return
                self.send_alert()
        else:
            check()
            self.send_alert()


    def send_alert(self):
        if self.msg_action != "silent" and self.config.silence_email is False:
            SendAMessage(self.msg_action,self.msg,self.config)


    def auto_run_schedule(self):
        now = self.config.build_time(0,"forward")

        # If the auto param is called, this loop will never be exited, until the job is
        # killed or the ctl-c. This program is designed to run continuously. 

        while True:
            if now >= self.config.start_time and now <= self.config.end_time: 
                while True:
                    if self.config.last_run == "never":
                        now = self.config.build_time(0,"forward")
                        # run health checks while waiting for first alert time slot
                        self.node_health(now)
                        if self.config.alert_interval > 60:
                            # lazy way out.
                            # if the interval is over 60 minutes, start on the quarter hour.
                            start_interval = 15
                        else:
                            start_interval = self.config.alert_interval

                        for n in range(0,60,start_interval):
                            if now.minute == n:
                                # set time first to avoid synchronous distortion
                                self.config.last_run = datetime.now(self.config.tz)
                                self.node_checkup()
                                break

                        if self.config.last_run != "never":
                            break
                        sleep(2)
                    else:
                        break

                while True:
                    now = self.config.build_time(0,"forward")

                    self.node_health(now)

                    next_run = self.config.last_run + timedelta(minutes=self.config.alert_interval)
                    next_run = next_run.strftime("%H:%M")
                    next_run = datetime.strptime(next_run,"%H:%M").time()
                    last_run = self.config.last_run.strftime("%H:%M")
                    last_run = datetime.strptime(last_run,"%H:%M").time()

                    if (now >= self.config.start_time and now <= self.config.report_time) and last_run < self.config.report_time: 
                        if now == self.config.report_time:
                            self.config.last_run = datetime.now(self.config.tz)
                            self.config.create_report = True
                            self.config.silence_writelog = True
                            self.node_checkup()
                        elif now >= next_run:
                            self.config.last_run = datetime.now(self.config.tz)
                            self.config.create_report = False
                            self.config.silence_writelog = False

                            if self.config.reload_needed():
                                # rebuild configuration because user modified
                                self.config = Config(self.config.dag_args)
                                break
                                
                            self.node_checkup()
                        sleep(2)
                    else:
                        break
            else:
                # force config back to alert settings to avoid reload_needed loop
                self.config = Config(self.config.dag_args) 
                # reset the last_run for next day (time slots)
                self.config.last_run = "never"
                now = self.config.build_time(0,"forward")
                # run health checks while waiting for alert run timezones
                self.node_health(now)
                sleep(2)


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")
