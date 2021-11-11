#!/bin/env python3
"""
MAIL_GRADE
Mun AI Lab Grading tool
"""
import argparse
import configparser
from pathlib import Path
from file_ops import initialize_assignment_directory, make_grade_template, copy_student_by_sid, save_gradefile_to_txt
from grades import Grades
from cli import mark_cli
from utils import *

if __name__ == '__main__':
    # ARGS
    parser = argparse.ArgumentParser()
    parser.add_argument('aname', help='the name of the subdirectory in the assignment directory')
    parser.add_argument('-i', "--init",
                        action="store_true",
                        help='Rename and remove old submission files, create a fresh output text file from a template')
    parser.add_argument('-t', "--template",
                        action='store_true',
                        help="Will look for a template file in the assignment directory with the substring 'mark' to use as a marking template.")
    parser.add_argument('-l', "--load", nargs=1,
                        help="Loads all files from the given student (by SID) into the source directory")
    parser.add_argument('-v', "--verbose",
                        action="store_true",
                        help='Prints directories and debug info to console')
    parser.add_argument('-m', "--mark",
                        action="store_true",
                        help="Begin marking the assignment. Init must be called first.")
    parser.add_argument('-g', "--gui",
                        action="store_true",
                        help="Enables GUI for marking.")
    parser.add_argument('-w', "--write",
                        action="store_true",
                        help="Writes the contents of grades.json to a text file.")
    parser.add_argument("--gradefile",
                        action="store_true",
                        help="Remakes the gradefile by scanning the submission directory looking for valid paths")
    args = parser.parse_args()
    a_name = args.aname

    # Arg switches
    # init initializes the assignment directory and creates a template file

    if args.verbose:
        set_verbose(True)

    if args.init:
        vprint(f"Initializing {a_name}")
        initialize_assignment_directory(a_name)
        if args.template:
            make_grade_template(a_name, gen_from_file=True)
        else:
            make_grade_template(a_name)

    # if just template is called, it remakes the grading template file
    #todo: if this is remade after the gradefile, it will probably be ignored
    if args.template and not args.init:
        make_grade_template(a_name, gen_from_file=True, remake=True)

    if args.gradefile:
        Grades(a_name, force_remake=True)

    if args.load:
        sid = args.load[0].lower()
        submission_path = Paths.get_submissions_path(a_name)
        source_path = Paths.get_source_path(a_name)
        copy_student_by_sid(submission_path, sid, source_path)

    if args.mark:
        grades = Grades(a_name)
        if args.gui:
            vprint("Marking with GUI")
            from ui.grader_ui_driver import GraderUiDriver, bind_window_and_run

            ui_driver = GraderUiDriver(grades)
            bind_window_and_run(ui_driver)
        else:
            vprint("Marking with CLI")
            mark_cli(grades)

    if args.write:
        vprint("Saving Gradefile to Text")
        out_file = Paths.get_data_path(a_name) / "grades.txt"
        gradefile_path = Paths.get_gradefile_path(a_name)
        if out_file.exists():
            out_file.unlink()
        save_gradefile_to_txt(gradefile_path, out_file)

    vprint("Done.")
