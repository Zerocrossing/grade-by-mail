verbose = False


def set_verbose(bool):
    global verbose
    verbose = bool


def vprint(str):
    if verbose:
        print(str)
    return


def grade_to_str(sid, data):
    s = f"{sid}:\n"
    for req, info in data.get("grade").items():
        s += f"{req}: {info.get('mark')}/{info.get('total')}\n"
    s += f"Comments:\n{data.get('comments')}\n"
    return s
