import os
from typing import Dict, List


def group_files_by_directory(files: List) -> Dict[str, List[str]]:
    """Group files by directory.

    :param files: A list of files.
    :return: A dict of files.
    """
    result: Dict[str, List[str]] = {}
    for file in files:
        dir_name = os.path.dirname(file)
        if dir_name not in result:
            result[dir_name] = []
        result[dir_name].append(file)
    return result


def filter_by_keywors(
    keyword_group: List[str], group_files: Dict[str, List[str]]
) -> Dict[str, List[str]]:
    """Filter files by keywords."""
    filter_group_files = {}
    for k, v in group_files.items():
        for keyeord in keyword_group:
            if k.find(keyeord) != -1:
                filter_group_files[k] = v
                continue
    return filter_group_files
