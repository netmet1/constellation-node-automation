from datetime import datetime, timedelta
import os
import yaml

class Config():

    def __init__(self,dag_args):

        self.dag_args = dag_args

        self.pull_configuration()
        self.setup_variables()
        self.setup_dates_times()
        self.setup_flags()
        self.config_default_check()


    def pull_configuration(self):
        self.config = {}
        self.path = os.path.dirname(__file__)
        self.config_file = self.path.replace("classes","configs/config.yaml")
        with open(self.config_file,'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
                self.config = self.config["configuration"]
            except yaml.YAMLError as exc:
                print(exc)


    def setup_dates_times(self):
        # defaults
        default_startdate_parameter = "07:00"  # for ease of reading/changing
        default_enddate_parameter = "20:00"    # for ease of reading/changing
        self.current_date = datetime.now().strftime("%Y-%m-%d")

        self.action = self.dag_args.Action

        try:
            start = datetime.strptime(self.config['intervals']['start_time'], "%H:%M")
        except:
            start = default_startdate_parameter
        try:
            end = datetime.strptime(self.config['intervals']['end_time'], "%H:%M")
        except:
            end = default_enddate_parameter

        if start > end:
            start = default_startdate_parameter
            end = default_enddate_parameter
        elif start == end:
            start = datetime.strptime("00:00", "%H:%M")
            end = datetime.strptime("23:50", "%H:%M") # leave time for report feature

        self.start_time = start - timedelta(minutes=start.minute % 15)
        self.end_time = end - timedelta(minutes=end.minute % 15)
        self.report_time_plus = self.end_time + timedelta(minutes=7)

        self.day_time_frame = f"{end.hour - start.hour} Hours {end.minute - start.minute} Minutes"
        self.day_run_hours = end.hour - start.hour


    def setup_variables(self):
        self.mms_email_recipients = self.config['email']['mms_recipients']
        self.email = self.config['email']['gmail_acct']
        self.token = self.config['email']['gmail_token']
        self.last_run = "never"
        self.error_max = self.config['constraints']['error_max']
        self.mem_swap_min = self.config['constraints']['memory_swap_min']
        self.username = self.config['email']['node_username']
        self.split1 = self.config['splits']['split1']
        self.split2 = self.config['splits']['split2']
        self.collateral_nodes = self.config['collateral']['node_count']
        self.report_estimates = self.config['report']['estimates']
        self.alert_interval = self.config['intervals']['int_minutes']


    def setup_flags(self):

        self.send_report = False

        if self.dag_args == "silent":
            self.silence_email = True
            self.silence_writelog = False
        else:
            self.silence_email = False
            self.silence_writelog = False    

        self.security_enabled= self.config['constraints']['security_check']
        self.splits_enabled = self.config['splits']['enabled']
        self.report_enabled = self.config['report']['enabled']
        self.collateral_enabled = self.config['collateral']['enabled']


    def config_default_check(self):
        try:
            int(self.error_max)
        except:
            self.error_max = 20
        else:
            if self.error_max == -1:
                self.error_max = 20

        try:
            int(self.mem_swap_min)
        except:
            self.mem_swap_min = 1000000
        else:
            if self.mem_swap_min == -1:
                self.mem_swap_min = 1000000
 
        try:
            int(self.alert_interval)
        except:
            self.alert_interval = 30  # default
        else:
            self.alert_interval = 5 * round(self.alert_interval/5) # round to nearest 5
            if self.alert_interval > 1440:
                self.alert_interval = 1440
            elif self.alert_interval < 10:
                self.alert_interval = 10

        try:
            float(self.split1)
        except:
            self.splits_enabled = False

        try:
            float(self.split2)
        except:
            self.splits_enabled = False

        try: 
            int(self.collateral_nodes)
        except:
            self.collateral_enabled = False

        if not isinstance(self.mms_email_recipients,list): 
            print("no recipients have been specified, or error in config.yaml.  Please see README.md")
            exit(1)

        if self.email == "" or self.email == None or not isinstance(self.email,str):
            print("no source sender email allocated in config.yaml. Please see README.md")
            exit(1)

        if self.token == "" or self.token == None or not isinstance(self.token,str):
            print("no source sender email token (password) allocated in config.yaml. Please see README.md")
            exit(1)

        if not isinstance(self.security_enabled,bool): 
            self.security_enabled = False

        if not isinstance(self.splits_enabled,bool): 
            self.splits_enabled = False

        if not isinstance(self.report_enabled,bool): 
            self.report_enabled = False

        if not isinstance(self.report_estimates,list): 
            if self.report_enabled:
                self.report_estimates = [.5,1,5,10,100]




