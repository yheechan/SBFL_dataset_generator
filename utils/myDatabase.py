

class myDatabase:
    def __init__(self):
        self.first = True

        # a dict with keys as file
        # a file holding info of cov per TC
        self.cov_per_file = {}

        # holds all TC information
        self.tc = {}
        self.name2id = {}

        # info of counts on TC
        self.tc_cnt = 0
        self.tf_cnt = 0
        self.tp_cnt = 0

        self.tc_criterion = {}
        self.tc_relation = {}
