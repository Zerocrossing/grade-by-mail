"""
Not an actual test suite, just a couple methods I wrote to quickly help me setup dummy projects for testing.
"""
from paths import get_assignment_path
from utils import *
import shutil
import argparse

RESTORE_DIR = "restore_test"
A_NAME = "test"

def restore_test(test_name):
    """
    Places the contents of ./data into the assignment directory
    Deletes all files that may have existed there previously
    Also clears any local data directory with the same name
    """
    restore_dir = Path("../test").resolve() / test_name
    copy_dir = Path(config.get("directories", "assignments")) / "test"
    print(f"Copying:\n\t{restore_dir}\n\t{copy_dir}")
    if copy_dir.exists():
        shutil.rmtree(copy_dir)
    shutil.copytree(restore_dir, copy_dir)

def print_paths(a_name):
    print(f"Assignment:\n\t{Paths.get_assignment_path(a_name)}")
    print(f"Grader:\n\t{Paths.get_grader_path(a_name)}")
    print(f"Grades:\n\t{Paths.get_grades_path(a_name)}")
    print(f"Submissions:\n\t{Paths.get_submissions_path(a_name)}")
    print(f"Restore:\n\t{Paths.get_restore_path(a_name)}")
    print(f"Config:\n\t{Paths.get_assignment_config_path(a_name)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', "--restore",
                        action="store_true",
                        help='Restores a directory from local data to the assignment directory for quick testing.')  
    parser.add_argument('-p', "--print",
                        action="store_true",
                        help='Prints the assignment directory path.')
    args = parser.parse_args()
    if args.restore:
        restore_test(RESTORE_DIR)
    if args.print:
        print_paths(A_NAME)
