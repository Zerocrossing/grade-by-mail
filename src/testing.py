"""
Not an actual test suite, just a couple methods I wrote to quickly help me setup dummy projects for testing.
"""
from utils import *
import shutil
import argparse

RESTORE_DIR = "restore_test"

def restore_test(test_name):
    """
    Places the contents of ./data into the assignment directory
    Deletes all files that may have existed there previously
    Also clears any local data directory with the same name
    """
    restore_dir = Path(config.get("directories", "data")) / test_name
    copy_dir = Path(config.get("directories", "assignments")) / "test"
    if copy_dir.exists():
        shutil.rmtree(copy_dir)
    shutil.copytree(restore_dir, copy_dir)
    #delete local test directory
    local_dir = Path(config.get("directories", "data")) / "test"
    if local_dir.exists():
        shutil.rmtree(local_dir)
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', "--restore",
                        action="store_true",
                        help='Restores a directory from local data to the assignment directory for quick testing.')
    
    args = parser.parse_args()
    if args.restore:
        restore_test(RESTORE_DIR)