import argparse
from classes.core import Core
from classes.config_obj import Config
from classes.logs import Logger

def retrieve_arguments():
    dag_parser = argparse.ArgumentParser(description="dag alerting script")

    dag_parser.add_argument('Action',
                            metavar='action',
                            type=str,
                            help="Type of action the script will run:\n(auto, alert, report, silent or log). Search dates (currently) only work with the \"log\" action.",
                            default="alert")
    dag_parser.add_argument("-p", "--print", help="print to the console instead of mms/sms, does not work with 'auto'.",
                            action="store_true")

    dag_parser.add_argument("-ss", "--search_start", 
                            help="Start date search log files for DAG balance at a certain date in time. Format: YYYY-MM-DD. This will supply the last entry recorded for the specified date. If search_end is not specified a single date will be searched.", 
                            type=str,
                            metavar="sdate")                    
    dag_parser.add_argument("-se", "--search_end", 
                            help="End date to search log files.  Format: YYYY-MM-DD", 
                            metavar="edate",
                            type=str)    

    return dag_parser.parse_args()

# ===================
# Start
# ===================


if __name__ == "__main__":
    dag_args = retrieve_arguments()

    config = Config(dag_args)
    core = Core(config)
    logger = Logger(config)

    if config.action == "auto":
        core.auto_run_schedule()
    elif config.action == "log":
        logger.process_request()
    else:
        core.node_checkup()