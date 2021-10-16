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
    reg = r'(.*) - (?P<sid>\w*)-(?P<name>.*) - (?P<date>.*, .{4}) (?P<time>.*)-(?P<fname>.*)'
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


def initialize_assignment_directory(submissions_path):
    """
    Scans through the submission directory
    Deletes duplicates based on submission date
    Prompts the user to delete submissions that don't conform to the D2L format
    Returns a list of path objects to valid paths
    :type submissions_path: pathlib.Path
    """
    submissions = {}  # holds objects with datetime and filename
    invalid_paths = []
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
        sid_name = f"{sid_name} {student_name}"  # used as a unique ID so we can access the name later

        # add file info to submissions
        if sid_name not in submissions:  # first time we see this student
            submissions[sid_name] = {file_name: {"date": submission_date, "path": f_path}}
        elif file_name not in submissions.get(sid_name):  # student seen, but new file
            submissions[sid_name].update({file_name: {"date": submission_date, "path": f_path}})
        else:  # duplicate filename, check dates
            prev_path = submissions.get(sid_name).get(file_name).get("path")
            prev_date = submissions.get(sid_name).get(file_name).get("date")
            if prev_date < submission_date:  # new file was submitted later, update info and delete previous
                submissions[sid_name][file_name] = {"date": submission_date, "path": f_path}
                vprint(
                    f"Deleting an old file because a newer one has been found:\n\tOld:\t{prev_path.name}\n\tNew:\t{f_path.name}")
                prev_path.unlink()
            else:  # new file is older, delete it
                vprint(
                    f"Deleting an old file because a newer one already exists:\n\tOld:\t{f_path.name}\n\tNew:\t{prev_path.name}")
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
        usrin = input("Do you want to delete these files? y/n")
        if usrin.lower() == "y":
            print("Deleting")
            [x.unlink() for x in invalid_paths]
    vprint(f"Initialization created {len(student_dirs)} submission directories in the assignment directory")
    return student_dirs


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


def make_grade_template(data_directory, template_directory=None):
    """
    given an assignment directory, looks for any files named "marks"
    prompts the user for which one, and calls parse_template to get a template dict
    template dict is written into the assignment directory as JSON
    :type data_directory: pathlib.Path
    """
    template = {"Grade": 100}
    template_path = data_directory / "marking_template.json"
    if template_directory is None:
        vprint(f"Creating a default template in {template_path}")
        json.dump(template, template_path.open('w+'))
        return template_path

    vprint(f"Looking for a marking template in {template_directory}")
    possible_templates = []
    for f_path in template_directory.iterdir():
        f_name = f_path.name.lower()
        if f_name.lower().find("marks") is not -1:
            possible_templates.append(f_path)
    if not possible_templates:
        raise Exception("No marking scheme found! Directory must contain a file with the word 'marks'")
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
    template_path = data_directory / "marking_template.json"
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


def save_gradefile_to_txt(gradefile_path, output_path):
    gradefile = json.load(gradefile_path.open('r'))
    txt = ""
    for sid, data in gradefile.items():
        s = grade_to_str(sid, data)
        txt += s
        partners = data.get("partners").lower()
        if partners is not "":
            partners = partners.split(",")
            for partner in partners:
                p_id = partner.strip()
                p_s = grade_to_str(p_id, data, is_partner=True)
                txt += p_s
    output_path.write_text(txt)
