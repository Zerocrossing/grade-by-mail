"""
File Operations
Saving, Loading, and Parsing local storage
"""
import re
import datetime
import json
import shutil
from zipfile import ZipFile
from pathlib import Path
from utils import *


def parse_d2l(filename):
    out = {}
    reg = r'(.*) - (?P<sid>\w+)-(?P<name>.+) - (?P<date>.+, .{4}) (?P<time>[^-]+)-(?P<fname>.*)'
    match = re.search(reg, filename)
    # parse time
    if match is None:
        return False
    time = match.group("time").split()
    hours = time[0][:-2]
    minutes = time[0][-2:]
    ampm = time[-1]
    time = hours + ":" + minutes + " " + ampm
    time_string = match.group("date") + ", " + time
    date_format = '%b %d, %Y, %I:%M %p'
    out["sid"] = match.group('sid')
    out["full_name"] = match.group("name")
    out["file_name"] = match.group('fname')
    out["date"] = datetime.datetime.strptime(time_string, date_format)
    return out


def _look_for_submission_zip(zip_path, dest_path):
    """
    Scans the directory looking for a zip file with 'download' , 'assignment' or 'submission' in the name
    Extracts the zip file to the destination path
    :type path: pathlib.Path
    """
    for fpath in zip_path.iterdir():
        if fpath.is_dir() or fpath.suffix != ".zip":
            continue
        matches = ["assignment", "download", "submission"]
        if any(x in fpath.name.lower() for x in matches):
            # unzip to destination
            vprint(f"Unzipping:\n\tsrc: {fpath}\n\tdst: {dest_path}")
            # vprint(f"Found submission zip file:\n{fpath}\nextracting to\n{dest_path}")
            zip_file = ZipFile(fpath, 'r')
            zip_file.extractall(dest_path)
            return True
    return False


def initialize_assignment_directory(a_name):
    """
    Creates the grader directory and subdirectories from config paths
    Scans through the submission directory
    Deletes duplicates based on submission date
    Prompts the user to delete submissions that don't conform to the D2L format
    :type submissions_path: pathlib.Path
    :type config: configparser.ConfigParser
    """
    # setup top level paths
    assignment_path = Paths.get_assignment_path(a_name)
    grader_path = Paths.get_grader_path(a_name)
    submissions_path = Paths.get_submissions_path(a_name)
    source_path = Paths.get_source_path(a_name)
    restore_path = Paths.get_restore_path(a_name)

    if not assignment_path.exists():
        raise FileNotFoundError(
            f"Assignment directory {assignment_path} does not exist")

    if not grader_path.exists():
        vprint(f"Making directory {grader_path}")
        grader_path.mkdir()

    # setup restore path
    make_restore_path(a_name)

    if not submissions_path.exists():
        vprint(f"Making directory {submissions_path}")
        submissions_path.mkdir()

    # setup grades path and subpaths for files in it
    grades_path = Paths.get_grades_path(a_name)
    if not grades_path.exists():
        vprint(f"Making directory {grades_path}")
        grades_path.mkdir()

    gradefile_path = Paths.get_gradefile_path(a_name)
    template_path = Paths.get_marking_template_path(a_name)

    # check for a zip file for submissions
    zip_found = _look_for_submission_zip(assignment_path, submissions_path)
    if not zip_found:
        raise FileNotFoundError(f"No D2L zip file found in {assignment_path}")

    submissions = {}  # holds objects with datetime and filename
    invalid_paths = []

    vprint("Deleting duplicate files...")
    for f_path in submissions_path.iterdir():
        suffix = f_path.suffix
        # parse d2l filename and get info
        file_info = parse_d2l(f_path.name)
        if not file_info:  # files that don't conform to d2l formatting
            invalid_paths.append(f_path)
            continue
        sid_name = file_info.get("sid")
        student_name = file_info.get("full_name")
        file_name = file_info.get("file_name")
        submission_date = file_info.get("date")
        # used as a unique ID so we can access the name later
        sid_name = f"{sid_name} {student_name}"

        # add file info to submissions
        if sid_name not in submissions:  # first time we see this student
            submissions[sid_name] = {file_name: {
                "date": submission_date, "path": f_path}}
        # student seen, but new file
        elif file_name not in submissions.get(sid_name):
            submissions[sid_name].update(
                {file_name: {"date": submission_date, "path": f_path}})
        else:  # duplicate filename, check dates
            prev_path = submissions.get(sid_name).get(file_name).get("path")
            prev_date = submissions.get(sid_name).get(file_name).get("date")
            if prev_date < submission_date:  # new file was submitted later, update info and delete previous
                submissions[sid_name][file_name] = {
                    "date": submission_date, "path": f_path}
                vprint(
                    f"\tOld:\t{prev_path.name}\n\tNew:\t{f_path.name}\n")
                prev_path.unlink()
            else:  # new file is older, delete it
                vprint(
                    f"\tOld:\t{f_path.name}\n\tNew:\t{prev_path.name}\n")
                f_path.unlink()
    student_dirs = []

    # rename and move all valid, recent submissions
    for sid_name, files in submissions.items():
        for f_name, data in files.items():
            path = data.get("path")
            parent = path.parent
            student_dir = parent / sid_name
            if not student_dir.is_dir():
                student_dir.mkdir()
            new_path = student_dir / f_name
            path.rename(new_path)
            if path.suffix == ".zip":
                _unzip_submission(new_path)
            if student_dir not in student_dirs and student_dir.exists():
                student_dirs.append(student_dir)

    # prompt user to remove any invalid files
    if invalid_paths:
        print("Invalid filenames found: ")
        [print(f"\t{x.name}") for x in invalid_paths]
        usrin = input("Do you want to delete these files? y/n ")
        if usrin.lower() == "y":
            print("Deleting")
            [x.unlink() for x in invalid_paths]
    vprint(
        f"Initialization created {len(student_dirs)} submission directories in the assignment directory")


def make_restore_path(a_name):
    """
    Creates the restore path if it doesn't exist
    :param source_path: pathlib.Path
    :param restore_path: pathlib.Path
    """
    if not config.getboolean("grading", "create_restore_dir"):
        vprint(f"Skipping restore directory creation")
        return

    restore_source_path = Paths.get_restore_source_path(a_name)
    restore_path = Paths.get_restore_path(a_name)

    if not restore_source_path.exists():
        raise FileNotFoundError(f"{restore_source_path} does not exist")

    if restore_path.exists():
        raise FileExistsError("{restore_path} Already exists")

    shutil.copytree(restore_source_path, restore_path)


def _unzip_submission(zip_path):
    """
    :type config: configparser.ConfigParser
    :type zip_path: pathlib.Path
    """
    ensure_dir = config.getboolean("zip", "ensure_dir")
    zip_dir = config.get("zip", "dir_name")
    delete = config.getboolean("zip", "delete_zip")
    zip = ZipFile(zip_path, 'r')
    for file_name in zip.namelist():
        if "/" not in file_name and ensure_dir:
            zip.extract(file_name, zip_path.parent / zip_dir)
        else:
            zip.extract(file_name, zip_path.parent)
    zip.close()
    if delete:
        zip_path.unlink()


def _parse_template(t_path):
    """
    takes the grades template file and extracts the grade information
    uses regex, might be weird
    returns a dict of rubrik components and their values
    template looks for lines with the format {TEXT} {dd/dd} where d is digits
    :type t_path: pathlib.Path
    """
    template = {}
    reg = r'(.+)\s(\S+)\/(\d+)'
    # reg = r'^(\S.+)\s(\S+)\/(\d+)' # this line excludes lines that start with whitespace, ie 'sub-categories'
    for line in t_path.open("r"):
        res = re.search(reg, line)
        if res:
            requirement = res.group(1).strip()
            if requirement[-1] == ':':
                requirement = requirement[:-1]
            value = res.group(3)
            template[requirement] = int(value)
    return template


def make_grade_template(a_name, gen_from_file=False, remake=False):
    """
    given an assignment directory, looks for any files named "marks"
    prompts the user for which one, and calls parse_template to get a template dict
    template dict is written into the assignment directory as JSON
    :type data_directory: pathlib.Path
    """
    template = {"Grade": 100}
    template_path = Paths.get_marking_template_path(a_name)
    # path to scan for a grade template .txt file
    template_text_dir = Paths.get_assignment_path(a_name)

    if template_path.exists() and not remake:
        vprint("Marking Template already exists, skipping creation")
        return

    if not template_path.exists() and not gen_from_file:
        vprint(f"Creating a default template in {template_path}")
        json.dump(template, template_path.open('w+'))
        return template_path

    vprint(f"Looking for a marking template in {template_text_dir}")
    possible_templates = []
    for f_path in template_text_dir.iterdir():
        f_name = f_path.name.lower()
        if f_name.lower().find("marks") != -1:
            possible_templates.append(f_path)
    if not possible_templates:
        raise Exception(
            "No marking scheme found! Directory must contain a file with the word 'marks'")
    in_bad = True
    template = {}
    while (in_bad):
        print("Please choose a template from the following options:")
        print("\t0:\tExit (abort and use no template)")
        for num, path in enumerate(possible_templates):
            print(f"\t{num + 1}\t{path.name}")
        usrin = input("Select an option: ")
        if not usrin.isdigit():
            continue
        else:
            choice = int(usrin)
            if choice == 0:
                raise Exception("No Suitable Template Found")
            if choice < 0 or choice > len(possible_templates):
                print("Invalid Selection\n")
            else:
                in_bad = False
                t_path = possible_templates[choice - 1]
                template = _parse_template(t_path)
    print("Template created:")
    [print(f"\t{k}: {v}%") for k, v in template.items()]
    json.dump(template, template_path.open('w+'))
    return template_path


def copy_student_by_sid(submission_dir, sid, src_dir):
    """
    :type src_dir: pathlib.Path
    :type submission_dir: pathlib.Path
    :type sid: pathlib.Path
    """
    # find subdir
    student_dir = None
    for fpath in submission_dir.iterdir():
        new_id, _, name = fpath.name.partition(" ")
        if sid == new_id:
            student_dir = fpath
            break
    # recursively iter and copy all files to new directory
    for path in student_dir.rglob('*'):
        if path.is_dir():
            continue
        if config.get("copying", "ignore_dotfiles"):
            if path.name[0] == '.':
                continue
        rel_path = path.relative_to(student_dir)
        dst_path = src_dir / rel_path
        if not dst_path.parent.exists():
            dst_path.parent.mkdir()
        vprint(f"Copying \n\t{path} to \n\t{dst_path}")
        shutil.copy(path, dst_path)


def restore_files(a_name):
    """
    type restore_path: pathlib.Path
    type source_path: pathlib.Path
    """
    restore_path = Paths.get_restore_path(a_name)
    source_path = Paths.get_restore_source_path(a_name)

    # copy all files from restore path to source path
    if not restore_path.exists():
        print("Restore path does not exist!")
        return
    for path in restore_path.rglob('*'):
        if path.is_dir():
            continue
        rel_path = path.relative_to(restore_path)
        dst_path = source_path / rel_path
        if not dst_path.parent.exists():
            dst_path.parent.mkdir()
        vprint(f"Copying \n\t{path} to \n\t{dst_path}")
        shutil.copy(path, dst_path)


def save_gradefile_to_txt(gradefile_path, output_path):
    gradefile = json.load(gradefile_path.open('r'))
    txt = ""
    for sid, data in gradefile.items():
        s = grade_to_str(sid, data)
        txt += s
        partners = data.get("partners").lower()
        if partners != "":
            partners = partners.split(",")
            for partner in partners:
                p_id = partner.strip()
                p_s = grade_to_str(p_id, data, is_partner=True)
                txt += p_s
    output_path.write_text(txt)
