"""
File Operations
Saving, Loading, and Parsing local storage
"""
import re
import datetime
import json
import shutil
from pathlib import Path
from utils import *


def initialize_assignment_directory(submissions_path):
    """
    Scans through the submission directory
    Deletes duplicates based on submission date
    Prompts the user to delete submissions that don't conform to the D2L format
    :type submissions_path: pathlib.Path
    """
    submissions = {}  # holds objects with datetime and filename
    invalid_paths = []
    # this ugly regex parses download names from the D2L batch download
    # todo move is_valid_d2l to new method for updating
    reg = r'(.*) - (?P<sid>\w*)-(?P<name>.*) - (?P<date>.*, .{4}) (?P<time>.*)-(?P<fname>.*)'
    for f_path in submissions_path.iterdir():
        match = re.search(reg, f_path.name)
        suffix = f_path.suffix
        if suffix is ".zip":
            # todo: handle unzipping
            pass
        if match is None:
            invalid_paths.append(f_path)
            continue
        # format the time string for datetime to parse
        time = match.group("time").split()
        time = time[0] + ":" + time[1] + " " + time[2]
        time_string = match.group("date") + ", " + time
        date_format = '%b %d, %Y, %I:%M %p'
        submission_date = datetime.datetime.strptime(time_string, date_format)
        # add file info to submissions
        sid = match.group('sid')
        file_name = match.group('fname')
        if sid not in submissions:  # first time we see this student
            submissions[sid] = {file_name: {"date": submission_date, "path": f_path}}
        elif file_name not in submissions.get(sid):  # student seen, but new file
            submissions[sid].update({file_name: {"date": submission_date, "path": f_path}})
        else:  # duplicate filename, check dates
            prev_path = submissions.get(sid).get(file_name).get("path")
            prev_date = submissions.get(sid).get(file_name).get("date")
            if prev_date < submission_date:  # new file was submitted later, update info and delete previous
                submissions[sid][file_name] = {"date": submission_date, "path": f_path}
                vprint(
                    f"Deleting an old file because a newer one has been found:\n\tOld:\t{prev_path.name}\n\tNew:\t{f_path.name}")
                prev_path.unlink()
            else:  # new file is older, delete it
                vprint(
                    f"Deleting an old file because a newer one already exists:\n\tOld:\t{f_path.name}\n\tNew:\t{prev_path.name}")
                f_path.unlink()
    valid_paths = []
    # rename all valid, recent submissions
    for sid, files in submissions.items():
        for f_name, data in files.items():
            path = data.get("path")
            parent = path.parent
            new_path = parent / f"{sid} {f_name}"
            path.rename(new_path)
            valid_paths.append(new_path)
    # prompt user to remove any invalid files
    if invalid_paths:
        print("Invalid filenames found: ")
        [print(f"\t{x.name}") for x in invalid_paths]
        usrin = input("Do you want to delete these files? y/n")
        if usrin.lower() == "y":
            print("Deleting")
            [x.unlink() for x in invalid_paths]
    vprint(f"Initialization found {len(valid_paths)} valid filenames in the assignment directory")
    return valid_paths


def _parse_template(t_path):
    """
    takes the grades template file and extracts the grade information
    uses regex, might be weird
    returns a dict of rubrik components and their values
    template looks for lines with the format {TEXT} {dd/dd} where d is digits
    :type t_path: pathlib.Path
    """
    template = {}
    reg = r'(\d+)/\d+'
    for line in t_path.open("r"):
        res = re.search(reg, line)
        if res:
            requirement = line[:res.start(0)].strip()
            value = res.group(1)
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


def swap_all_files_by_id(submissions_path, id, src_path):
    """
    copies all files prepended with the supplied ID to ./path/src
    :type src_path: pathlib.Path
    """
    loaded = False
    for f_path in submissions_path.iterdir():
        f_name = f_path.name
        f_id = f_path.name.lower().split()[0]
        if f_id == id:
            real_filename = f_name.replace(f_id, "").strip()
            loaded = True
            dst_path = src_path / real_filename
            shutil.copy(f_path, dst_path)
            vprint(f"Copied \n{f_name}\nTo:\n{dst_path.name}")
    if not loaded:
        raise Exception("No student files with that name found. Have you initialized the files?")

def swap_single_file(file_path, dst_path):
    """
    :type file_path: pathlib.Path
    :type dst_path: pathlib.Path
    """
    # can handle strings
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    if not isinstance(dst_path, Path):
        file_path = Path(dst_path)
    sid, _, real_filename = file_path.name.partition(" ")
    shutil.copy(file_path, dst_path/ real_filename)
    vprint(f"Copied \n{file_path}\nTo:\n{dst_path}")

def save_gradefile_to_txt(gradefile_path, output_path):
    gradefile = json.load(gradefile_path.open('r'))
    txt = ""
    for sid, data in gradefile.items():
        s = grade_to_str(sid, data)
        txt += s
        partners = data.get("partners")
    output_path.write_text(txt)
    #todo stopped here last night
