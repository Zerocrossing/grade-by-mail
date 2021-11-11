from utils import *

def get_assignment_path(a_name):
    """
    Returns the path to the main assignment directory
    """
    root_dir = Path(config.get("directories", "assignments"))
    assignment_path = root_dir / a_name
    return assignment_path

def get_submissions_path(a_name):
    """
    Returns the path to the submissions subdirectory of the assignment directory
    """
    assignment_path = get_assignment_path(a_name)
    submissions_path = assignment_path / config.get("directories", "submissions")
    return submissions_path

def get_source_path(a_name):
    """
    Returns the path to the source subdirectory of the assignment directory
    This is where student submissions are copied to
    """
    assignment_path = get_assignment_path(a_name)
    source_path = assignment_path / config.get("directories", "source")
    return source_path

def get_restore_path(a_name):
    """
    Returns the path to the restore subdirectory of the assignment directory
    This path is a blank copy of the source directory
    """
    assignment_path = get_assignment_path(a_name)
    restore_path = assignment_path / config.get("directories", "restore")
    return restore_path

def get_data_path(a_name):
    """
    Returns the path to the local data path, where the grades are stored
    """
    data_path = Path(config.get("directories", "data")) / a_name
    return data_path

def get_gradefile_path(a_name):
    """
    Returns the path to the local gradefile json file
    """
    data_path = get_data_path(a_name)
    gradefile_path = data_path / "grades.json"
    return gradefile_path
    
def get_marking_template_path(a_name):
    """
    Returns the path to the local marking template json file
    """
    data_path = get_data_path(a_name)
    gradefile_path = data_path / "marking_template.json"
    return gradefile_path

if __name__ == "__main__":
    a_name = "A3"
    print(f"Assignment path: {get_assignment_path(a_name)}")
    print(f"Submissions path: {get_submissions_path(a_name)}")
    print(f"Source path: {get_source_path(a_name)}")
    print(f"Restore path: {get_restore_path(a_name)}")
    print(f"Data path: {get_data_path(a_name)}")
    print(f"Gradefile path: {get_gradefile_path(a_name)}")
    print(f"Marking template path: {get_marking_template_path(a_name)}")
    # print(get_submissions_path(a_name))
    # print(get_source_path(a_name))
    # print(get_restore_path(a_name))
    # print(get_data_path(a_name))
    # print(get_gradefile_path(a_name))
    # print(get_marking_template_path(a_name))
