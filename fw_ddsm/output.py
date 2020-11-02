import pandas_bokeh
from pathlib import Path
from pandas import DataFrame as df
from datetime import date, datetime
from fw_ddsm.parameter import *
from fw_ddsm.tracker import *


class Show:

    def __init__(self):

        self.scheduling_method = ""
        self.pricing_method = ""
        self.output_folder = ""
        self.aggregator_tracker = Tracker()
        self.community_tracker = Tracker()

    def set_output_folder(self, output_folder):
        this_date = str(date.today())
        this_time = str(datetime.now().time().strftime("%H-%M-%S"))
        output_folder = output_folder if output_folder.endswith("/") else output_folder + "/"
        self.output_folder = f"{output_folder}{this_date}/{this_time}/"
        path = Path(self.output_folder)
        if not path.exists():
            path.mkdir(mode=0o777, parents=True, exist_ok=False)
        return self.output_folder

    def set_data(self, algorithm, aggregator_tracker, community_tracker=None):
        self.aggregator_tracker = Tracker()
        self.community_tracker = Tracker()
        self.scheduling_method = algorithm[k2_before_fw]
        self.pricing_method = algorithm[k2_after_fw]
        self.aggregator_tracker = aggregator_tracker
        self.community_tracker = community_tracker

    def draw_graphs(self):
        return 0


