import argparse
from datetime import datetime, timedelta
from time import sleep

from classes.error_log_check import ErrorLogCheck 
from classes.check_dag_status import CheckDagStatus
from classes.send_sms_email import SendAMessage
from classes.reports import CreateReport
from classes.config_obj import Config

def retrieve_arguments():
    dag_parser = argparse.ArgumentParser(description="dag alerting script")

    dag_parser.add_argument('Action',
                            metavar='action',
                            type=str,
                            help="type of action the script will run (auto, alert, report, or silent)",
                            default="alert")

    return dag_parser.parse_args()


def node_checkup(config,send_report=False):
    
    if send_report:
        config.send_report = True
        config.silence_writelog = True
    else:
        config.send_report = False
        config.silence_writelog = False

    checkForErrors = ErrorLogCheck(config)
    buildReport = CheckDagStatus(config)

    if checkForErrors.error_count > config.error_max:
        msg = checkForErrors.error_report_body+"\n\n"+buildReport.report_body
        msg_action = "error"
    else:
        msg = buildReport.report_body
        msg_action = "normal"

    if config.action == "report" or send_report is True:
        if config.report_enabled is True:
            createReport = CreateReport("daily", buildReport.usd_dag_price, config)
            msg = createReport.report_str 
        else:
            msg_action = "silent"

    if msg_action != "silent" and config.silence_email is False:
        SendAMessage(msg_action,msg,config)


def auto_run_schedule(config):
    now = datetime.now().strftime("%H:%M")
    now = datetime.now().strptime(now,"%H:%M").time()

    # If the auto param is called, this loop will never be exited, until the job is
    # killed or the ctl-c. This program is designed to run continuously. 
    while True:
        if now >= config.start_time and now <= config.end_time: 
            while True:
                if config.last_run == "never":
                    now = datetime.now().strftime("%H:%M")
                    now = datetime.now().strptime(now,"%H:%M").time()
                    if config.alert_interval > 60:
                        # lazy way out.
                        # if the interval is over 60 minutes, start on the quarter hour.
                        start_interval = 15
                    else:
                        start_interval = config.alert_interval

                    for n in range(0,60,start_interval):
                        if now.minute == n:
                            # set time first to avoid synchronous distortion
                            config.last_run = datetime.now()
                            node_checkup(config)
                            break

                    if config.last_run != "never":
                        break
                    sleep(2)
                else:
                    break

            # print(f"config.last_run: {config.last_run}")

            while True:
                now = datetime.now().strftime("%H:%M")
                now = datetime.now().strptime(now,"%H:%M").time()
                next_run = config.last_run + timedelta(minutes=config.alert_interval)
                next_run = next_run.strftime("%H:%M")
                next_run = datetime.strptime(next_run,"%H:%M").time()
                last_run = config.last_run.strftime("%H:%M")
                last_run = datetime.strptime(last_run,"%H:%M").time()

                if (now >= config.start_time and now <= config.report_time) and last_run < config.report_time: 
                    if now == config.report_time:
                        print("report time")
                        config.last_run = datetime.now()
                        node_checkup(config,True)
                    elif now >= next_run:
                        config.last_run = datetime.now()
                        node_checkup(config)
                    sleep(2)
                else:
                    break

        else:
            config.last_run = config.start_time - timedelta(minutes=15)
            now = datetime.now().strftime("%H:%M")
            now = datetime.now().strptime(now,"%H:%M").time()
            sleep(2)


# ===================
# Start
# ===================


if __name__ == "__main__":
    dag_args = retrieve_arguments()
    config = Config(dag_args)

    if config.action == "auto":
        auto_run_schedule(config)
    else:
        if config.action == "report":
            node_checkup(config,True)
        else:
            node_checkup(config)

