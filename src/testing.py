"""
Not an actual test suite, just a couple methods I wrote to quickly help me setup dummy projects for testing.
"""
from utils import *
import shutil
import argparse

RESTORE_DIR = "testa3"

def restore_test(test_path):
    """
    Places the contents of ./data into the assignment directory
    Deletes all files that may have existed there previously
    """
    restore_dir = Path(config.get("directories", "data")) / test_path
    copy_dir = Path(config.get("directories", "assignments")) / test_path
    if copy_dir.exists():
        shutil.rmtree(copy_dir)
    shutil.copytree(restore_dir, copy_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', "--restore",
                        action="store_true",
                        help='Restores a directory from local data to the assignment directory for quick testing.')
    
    args = parser.parse_args()
    if args.restore:
        restore_test(RESTORE_DIR)