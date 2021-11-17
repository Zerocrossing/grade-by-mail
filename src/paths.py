from utils import *


def get_assignment_path(a_name):
    """
    Returns the path to the main assignment directory
    This is considered the top level directory, and is given by the command line
    """
    root_dir = Path(config.get("directories", "assignments"))
    assignment_path = root_dir / a_name
    return assignment_path


def get_grader_path(a_name):
    """
    Returns the path to the grader directory
    Located in /assignment/grader/
    """
    a_dir = get_assignment_path(a_name)
    grader_path = a_dir / config.get("directories", "grader")
    return grader_path


def get_grades_path(a_name):
    """
    Returns the path to the grades subdirectory of the grader directory
    Located in /assignment/grader/grades by default
    """
    assignment_path = get_assignment_path(a_name)
    grades_path = assignment_path / config.get("directories", "grades")
    return grades_path


def get_gradefile_path(a_name):
    """
    Returns the path to the gradefile json file
    Located in /assignment/grader/grades/gradefile.json
    """
    grades_path = get_grades_path(a_name)
    gradefile_path = grades_path / "grades.json"
    return gradefile_path


def get_submissions_path(a_name):
    """
    Returns the path to the submissions subdirectory of the assignment directory
    Located in /assignment/grader/submissions
    """
    assignment_path = get_assignment_path(a_name)
    submissions_path = assignment_path / \
        config.get("directories", "submissions")
    return submissions_path


def get_assignment_config_path(a_name):
    """
    Returns the path to the assignment config file
    Located in /assignment/grader/config.ini
    """
    assignment_path = get_assignment_path(a_name)
    config_path = assignment_path / config.get("directories", "config")
    return config_path


def get_source_path(a_name):
    """
    Returns the path to the source subdirectory of the assignment directory
    This is where student submissions are copied to
    Located in /assignment/source
    """
    assignment_path = get_assignment_path(a_name)
    source_path = assignment_path / config.get("directories", "source")
    return source_path


def get_restore_path(a_name):
    """
    Returns the path to the restore subdirectory of the assignment directory
    This path is a blank copy of the source directory, created on initialization
    Located in /assignment/grader/restore
    """
    assignment_path = get_assignment_path(a_name)
    restore_path = assignment_path / config.get("directories", "restore")
    return restore_path


def get_restore_source_path(a_name):
    """
    Returns the path to be copied into the restore directory
    This will usually be the same as the source directory, but may not
    For example, if students are submissing a subdirectory that is placed in the main assignment directory,
    This will be that subdirectory, but the source path will be the main assignment directory
    """
    assignment_path = get_assignment_path(a_name)
    restore_source_path = assignment_path / \
        config.get("directories", "restore_source")
    return restore_source_path


def get_marking_template_path(a_name):
    """
    Returns the path to the local marking template json file
    Located in /assignment/grader/grades/marking_template.json
    """
    grades_path = get_grades_path(a_name)
    marking_template_path = grades_path / "marking_template.json"
    return marking_template_path


if __name__ == "__main__":
    a_name = "test"
    print(f"Assignment path:\n\t{get_assignment_path(a_name)}")
    print(f"Grader path:\n\t{get_grader_path(a_name)}")
    print(f"Grades path:\n\t{get_grades_path(a_name)}")
    print(f"Gradefile path:\n\t{get_gradefile_path(a_name)}")
    print(f"Submissions path:\n\t{get_submissions_path(a_name)}")
    print(f"Restore source path:\n\t{get_restore_source_path(a_name)}")
    print(f"Restore path:\n\t{get_restore_path(a_name)}")
    print(f"Assignment config path:\n\t{get_assignment_config_path(a_name)}")
    print(f"Source path:\n\t{get_source_path(a_name)}")
    print(f"Marking template path:\n\t{get_marking_template_path(a_name)}")
