import argparse
from classes.core import Core
from classes.config_obj import Config

def retrieve_arguments():
    dag_parser = argparse.ArgumentParser(description="dag alerting script")

    dag_parser.add_argument('Action',
                            metavar='action',
                            type=str,
                            help="type of action the script will run (auto, alert, report, or silent)",
                            default="alert")

    return dag_parser.parse_args()

# ===================
# Start
# ===================


if __name__ == "__main__":
    dag_args = retrieve_arguments()
    config = Config(dag_args)
    core = Core(config)

    if config.action == "auto":
        core.auto_run_schedule()
    else:
        if config.action == "report":
            core.node_checkup(True)
        else:
            core.node_checkup()