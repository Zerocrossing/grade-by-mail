"""
Grades
A bit of a god class, it's a wrapper around the json gradefile
"""
from utils import *
import json
from pathlib import Path
# GUI_LOADED = True
# try:
#     from PySide2.QtWidgets import QWidget
# except ImportError:
#     vprint("GUI library not found")
#     GUI_LOADED = False


class Grades:
    def __init__(self, gradefile_path, template_path, submissions_path, source_path, valid_filepaths=None):
        """
        Providing valid_filepaths (which are created during initialization) will allow unformatted files to exist in the
            submission directory without being considered. Otherwise all files are assumed to have been formatted
            by initialize_assignment_directory in file_ops.py
        :type submissions_path: pathlib.Path
        :type template_path: pathlib.Path
        :type gradefile_path: pathlib.Path
        """
        self.gradefile_path = gradefile_path
        self.template_path = template_path
        self.submissions_path = submissions_path
        self.source_path = source_path
        self.valid_filepaths = valid_filepaths
        self.data = {}
        self.make_gradefile()
        self.template = json.load(template_path.open('r'))
        # marking vars
        self.sids = list(self.data.keys())
        self.total = len(self.sids)
        self.curr = 0


    def make_gradefile(self):
        if self.gradefile_path.exists():
            vprint(f"Loading gradefile from {self.gradefile_path}")
            self.data = json.load(self.gradefile_path.open('r'))
            return
        if self.valid_filepaths is not None:
            vprint(f"Making grade file from a list of valid paths")
            for f_path in self.valid_filepaths:
                self.add_path_to_data(f_path)
        else:
            vprint(f"Making grade file for all files in {self.submissions_path}")
            for f_path in self.submissions_path.iterdir():
                self.add_path_to_data(f_path)
        self.save()

    def add_path_to_data(self, path):
        """
        Adds the given path to the gradedata file
        Assumes the filename is already formatted
        :type path: pathlib.Path
        """
        vprint(f"Adding {path.name} to the grade file")
        sid, _, f_name = path.name.partition(" ")
        # first time seeing student
        if sid not in self.data:
            self.data[sid] = {
                "files": [],
                "grade": {},
                "partners": "",
                "comments": "",
                "marked": False
            }
            template = json.load(self.template_path.open('r'))
            for requirement, value in template.items():
                self.data[sid]["grade"][requirement] = {"mark": None, "total": value}
        path_str = str(path)
        self.data[sid]["files"].append(path_str)

    def save(self):
        vprint(f"Saving gradefile to {self.gradefile_path}")
        json.dump(self.data, self.gradefile_path.open('w+'))

    def load(self):
        vprint(f"Loading gradefile from {self.gradefile_path}")
        self.data = json.load(self.gradefile_path.open('r'))

    def cur_id(self):
        return self.sids[self.curr]

    def next(self):
        if self.curr < self.total:
            self.curr += 1

    def prev(self):
        if self.curr >0:
            self.curr -= 1

    def curr_data(self):
        return self.data[self.cur_id()]

    def progress(self):
        """
        returns a value from 0-100 representing how many students are 'marked'
        """
        marked =0
        for sid, data in self.data.items():
            if data.get("marked"):
                marked += 1
        return (marked / self.total) *100

if __name__ == '__main__':
    p = Path("rwb95 config file.txt")
    sid, _, f_name = p.name.partition(" ")
    print(f"sid: {sid}\nfname: {f_name}")

    # a_name = "a1backup"
    # gfp = Path("../data/a1backup/grades.json")
    # grades = Grades()
