import configparser

# evil globals and such
verbose = False
config = configparser.ConfigParser()
config.read("config.ini")


def set_verbose(bool):
    global verbose
    verbose = bool


def vprint(str):
    if verbose:
        print(str)
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
            mark = "??"
        if total is None:
            total = "??"
        s += f"{req:{max_len}}: {mark:0>2}/{total:0>2}\n"
    s += f"Comments:\n{data.get('comments')}\n\n"
    return s
