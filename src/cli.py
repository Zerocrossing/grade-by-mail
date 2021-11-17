import os
from grades import Grades
from utils import *


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def grade_string(grades):
    """
    Returns a nicely formatted string presenting all the grade info on the current student
    :type grades: Grades
    """
    bar = "*" * 36 + '\n'
    data = grades.curr_data()
    sid = grades.cur_id()
    full_name = grades.curr_name()
    status = "(incomplete)"
    if data.get("marked"):
        status = "(complete)"
    progress = f"{grades.curr+1}/{grades.total+1}"
    nameplate = f"{sid}-{full_name} {status}\t{progress}"
    out = f"{bar}{nameplate}\n{bar}"
    out += "Grades:\n"
    for req, mark_obj in data.get("grade").items():
        g = mark_obj.get("mark")
        if g is None:
            g = "?"
        t = mark_obj.get("total")
        out += f"\t{req}:\t\t{g}/{t}\n"
    out += f"Partners: {data.get('partners')}\n"
    out += f"Comments: {data.get('comments')}"
    return out.strip()


def print_options():
    print("""
Select an Option:
    l: load files
    r: restore files
    s: save to disk
    g: edit grades
    p: edit partner
    c: add a comment
    t: toggle completion status
    >: next
    <: prev
    q: quit    
    """)


def next_grade(grades):
    """
    :type grades: grades.Grades
    """
    grades.next()


def add_comment(grades):
    usrin = input("Write a comment:\n")
    grades.curr_data()["comments"] = usrin


def edit_partner(grades):
    usrin = input("Enter the student ID of one or more partners, separated by comas:\n")
    grades.curr_data()["partners"] = usrin


def edit_grades(grades):
    """
    :type grades: grades.Grades
    """
    grade = grades.curr_data().get("grade")
    for req, mark_obj in grades.curr_data().get("grade").items():
        in_bad = True
        while (in_bad):
            cls()
            print(grade_string(grades))
            prompt = f"Enter a grade for {req} or s to skip:"
            if "total" in req.lower(): prompt += " (press t for auto-total)"
            print(prompt)
            usrin = input().lower()
            if usrin.isdigit():
                grades.curr_data()["grade"][req]["mark"] = int(usrin)
                in_bad = False
            if usrin == 's':
                break
            if usrin == 't':
                total = 0
                for r, o in grades.curr_data().get("grade").items():
                    v = o.get("mark")
                    if v is not None:
                        total += v
                grades.curr_data()["grade"][req]["mark"] = total
                in_bad = False


def mark_cli(grades):
    """
    type grades: Grades
    """
    while (True):
        cls()
        print(grade_string(grades))
        print_options()
        usrin = input()
        if usrin == 'l':
            grades.copy_current()
            cls()
            input(f"Loaded files by {grades.cur_id()} to source directory. Enter to continue...")
        if usrin == 'r':
            grades.restore()
            cls()
            input(f"Copied all files from->to: \n\t{grades.restore_path}\n\t{grades.source_path}\nEnter to continue...")
        if usrin == 'g':
            edit_grades(grades)
        if usrin == 's':
            grades.save()
        if usrin == 'p':
            edit_partner(grades)
        if usrin == 'c':
            add_comment(grades)
        if usrin == 't':
            data = grades.curr_data()
            data["marked"] = not data["marked"]
        if usrin == '>':
            grades.next()
        if usrin == '<':
            grades.prev()
        if usrin == 'q':
            quit()
