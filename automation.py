# ======================================
# 
#  Constellation Node Automation Program
#  
#  last update:  2021-08
#  author:  hgtp://netmet
#
#  DISCLAIMER:  I do not work for 
#  Constellation Network however I am
#  a proud member of the community and
#  this is just a script to help the 
#  community.
#
#  Version 2.0
# ===================================== 

import argparse
from classes.core import Core
from classes.config_obj import Config
from classes.logs import Logger

def retrieve_arguments(version="2.0"):
    dag_parser = argparse.ArgumentParser(description="dag alerting script")

    dag_parser.add_argument('Action',
                            metavar='ACTION',
                            type=str,
                            help="Type of action the script will run:\n(auto, alert, report, health, silent or log). Search dates (currently) only work with the \"log\" action.",
                            default="alert")
    dag_parser.add_argument("-p", "--print", help="print to the console instead of mms/sms/email, does not work with 'auto'.",
                            action="store_true")

    dag_parser.add_argument("-c", "--csv", 
                            metavar='EMAIL',
                            type=str,
                            default=False,
                            help="For use with the 'log' action only.  Program will send a csv formatted file with search results to the specified email.")

    dag_parser.add_argument("-ss", "--search_start", 
                            help="For use with 'log' action. The start date search log files for DAG balance at a certain date in time. Format: YYYY-MM-DD. This will supply the last entry recorded for the specified date. If search_end is not specified a single date will be searched.", 
                            type=str,
                            default=False,
                            metavar="START_DATE")                    
    dag_parser.add_argument("-se", "--search_end", 
                            help="For use with 'log' action. The end date to search log files.  Format: YYYY-MM-DD", 
                            metavar="END_DATE",
                            default=False,
                            type=str)    
    dag_parser.add_argument('-v','--version', action='version', version=f'%(prog)s version: {version}')  

    return dag_parser.parse_args()

# ===================
# Start
# ===================


if __name__ == "__main__":
    dag_args = retrieve_arguments()
    config = Config(dag_args)

    if config.action == "log":
        logger = Logger(config)
        logger.process_request()
    else:
        core = Core(config)
        if config.action == "auto":
            core.auto_run_schedule()
        elif config.action == "health":
            core.node_health()
        else:
            core.node_checkup()