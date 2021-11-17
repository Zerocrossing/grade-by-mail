import configparser
from pathlib import Path
import os

# evil globals and such
verbose = False
config = configparser.ConfigParser()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
config.read("./config.ini")
import paths as Paths


def set_verbose(bool):
    global verbose
    verbose = bool
    if bool:
        print("Verbose mode enabled")


def vprint(str):
    if verbose:
        print(str)
    return

def banner_print(str, char="*"):
    print('\n'+char*(len(str)+4))
    title = str.center(len(str)+2)
    print(f"{title}".center(len(str)+4, char))
    print(char*(len(str)+4)+'\n')

def vbanner_print(str, char="*"):
    if verbose:
        banner_print(str, char)
    return

def grade_to_str(sid, data, is_partner=False):
    s = ""
    if not is_partner:
        s = f"{sid} {data.get('full_name')}:\n"
    else:
        s = f"{sid}:\n"
    max_len = 16
    for req, info in data.get("grade").items():
        if len(req) >= max_len: max_len = len(req)+1
    for req, info in data.get("grade").items():
        mark = info.get('mark')
        total = info.get('total')
        # None is the default value, meaning this student hasn't been marked yet
        if mark is None:
            continue
            mark = "??"
        if total is None:
            total = "??"
        s += f"{req:{max_len}}: {mark:0>2}/{total:0>2}\n"
    s += f"Comments:\n{data.get('comments')}\n\n"
    return s