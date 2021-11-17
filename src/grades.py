"""
Grades
A bit of a god class, it's a wrapper around the json gradefile
"""
from utils import *
import json
from pathlib import Path
from file_ops import copy_student_by_sid, restore_files


class Grades:

    def __init__(self, assignment_name, force_remake=False):
        """
        Creates grades object from config
        type config: configparser.ConfigParser()
        """
        self.grader_path = Paths.get_grader_path(assignment_name)
        if not self.grader_path.exists():
            print(
                "ERROR: No grader directory exists. Ensure you run initialization before attempting to mark.\n")
            raise FileNotFoundError(self.grader_path)
        self.assignment_name = assignment_name
        self.gradefile_path = Paths.get_gradefile_path(assignment_name)
        self.template_path = Paths.get_marking_template_path(assignment_name)
        self.submissions_path = Paths.get_submissions_path(assignment_name)
        self.source_path = Paths.get_source_path(assignment_name)
        self.student_dirs = None
        self.restore_path = Paths.get_restore_path(assignment_name)
        self.data = {}
        self.make_gradefile(force_remake)
        self.template = json.load(self.template_path .open('r'))
        self.sids = list(self.data.keys())
        self.total = len(self.sids) - 1
        self.curr = 0

    def make_gradefile(self, force_remake):
        if self.gradefile_path.exists() and not force_remake:
            vprint(f"Loading gradefile from {self.gradefile_path}")
            self.data = json.load(self.gradefile_path.open('r'))
            return
        if self.student_dirs is not None:
            vprint(f"Making grade file from a list of valid paths")
            for f_path in self.student_dirs:
                self.add_path_to_data(f_path)
        else:
            vprint(
                f"Making grade file for all files in {self.submissions_path}")
            for f_path in self.submissions_path.iterdir():
                self.add_submission_path(f_path)
                # self.add_path_to_data(f_path)
        self.save()

    def add_submission_path(self, submission_path):
        """
        Adds the student path to the gradefile
        """
        if not submission_path.is_dir():
            return
        sid, _, student_name = submission_path.name.partition(" ")
        # first time seeing student
        if sid in self.data:
            raise ValueError(f"Student {sid} already exists in gradefile")

        # make empty grade object
        self.data[sid] = {
            "full_name": student_name,
            "submission_path": str(submission_path),
            "grade": {},
            "partners": "",
            "comments": "",
            "marked": False
        }
        # add marks
        template = json.load(self.template_path.open('r'))
        for requirement, value in template.items():
            self.data[sid]["grade"][requirement] = {
                "mark": None, "total": value}

    def save(self):
        vprint(f"Saving gradefile to {self.gradefile_path}")
        json.dump(self.data, self.gradefile_path.open('w+'))

    def load(self):
        vprint(f"Loading gradefile from {self.gradefile_path}")
        self.data = json.load(self.gradefile_path.open('r'))

    def restore(self):
        vprint(
            f"Restoring all files from {self.restore_path} to  {self.source_path}")
        restore_files(self.assignment_name)

    def copy_current(self):
        copy_student_by_sid(self.submissions_path,
                            self.cur_id(), self.source_path)

    def cur_id(self):
        return self.sids[self.curr]

    def curr_name(self):
        return self.data[self.cur_id()]["full_name"]

    def next(self):
        if self.curr < self.total:
            self.curr += 1

    def prev(self):
        if self.curr > 0:
            self.curr -= 1

    def curr_data(self):
        return self.data[self.cur_id()]

    def progress(self):
        """
        returns a value from 0-100 representing how many students are 'marked'
        """
        marked = 0
        for sid, data in self.data.items():
            if data.get("marked"):
                marked += 1
        val = (marked / (self.total+1)) * 100
        return val
