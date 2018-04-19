import os
from constants import *


def check_path_exists():
    base_path_checks = [csv_dir, json_dir]
    csv_path_checks = {csv_dir: [csv_source_dir, csv_parsed_dir, csv_clean_dir, csv_updated_dir]}

    for paths in base_path_checks:
        if not os.path.exists(paths):
            os.path.join(base_dir, paths)

    for csv_base_dir, csv_sub_dir in csv_path_checks.items():
        for i in csv_sub_dir:
            if not os.path.exists(i):
                os.makedirs(i)

if __name__ == '__main__':
    check_path_exists()