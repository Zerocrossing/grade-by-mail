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
    args = parser.parse_args()
    a_name = args.aname

    # Config Values
    config = configparser.ConfigParser()
    config.read("config.ini")
    root_dir = Path(config.get("directories", "assignments"))
    assignment_dir = root_dir / a_name
    source_dir = assignment_dir / config.get('directories', 'source')
    submissions_dir = assignment_dir / config.get("directories", "submissions")
    data_dir = Path(config.get("directories", "data")) / a_name
    if not data_dir.exists():
        vprint(f"{data_dir} not found! Creating...")

    # Arg paths
    if args.verbose:
        set_verbose(True)
        vprint("Loading Directories from Config File: ")
        vprint(f"\tRoot Directory: \t{root_dir}")
        vprint(f"\tAssignment Directory: \t{assignment_dir}")
        vprint(f"\tSource Directory: \t{source_dir}")
        vprint(f"\tSubmissions Directory: \t{submissions_dir}")
        vprint(f"\tLocal Data Directory: \t{data_dir}")

    gradefile_path = data_dir / "grades.json"
    template_path = data_dir / "marking_template.json"

    # Init cleans the submission file directory, then makes a template and a gradefile
    if args.init:
        vprint(f"Initializing {a_name}")
        template = args.template
        if not data_dir.exists():
            vprint(f"{data_dir} not found! Creating...")
            data_dir.mkdir()
        valid_paths = initialize_assignment_directory(submissions_dir)
        template_path = None
        # todo, check for pre-existing template file, or maybe create and 'update gradefile' method
        if not args.template:
            template_path = make_grade_template(data_dir)
        if args.template:
            template_path = make_grade_template(data_dir, template_directory=assignment_dir)
        grades = Grades(gradefile_path, template_path, submissions_dir, source_dir, student_dirs=valid_paths)

    if args.template and not args.init:
        make_grade_template(data_dir, template_directory=assignment_dir)

    if args.load:
        sid = args.load[0].lower()
        copy_student_by_sid(submissions_dir, sid, source_dir)

    if args.mark:
        # todo
        print(f"Data type of template path: {template_path}, {type(template_path)}")
        grades = Grades(gradefile_path, template_path, submissions_dir, source_dir)
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
        save_gradefile_to_txt(gradefile_path, data_dir / "grades.txt")

    vprint("Done.")
