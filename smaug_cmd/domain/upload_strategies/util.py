from typing import Dict, List


def filter_by_keywors(
    keyword_group: List[str], group_files: Dict[str, List[str]]
) -> Dict[str, List[str]]:
    filter_group_files = {}
    for k, v in group_files.items():
        for keyeord in keyword_group:
            if k.find(keyeord) != -1:
                filter_group_files[k] = v
                continue
    return filter_group_files
