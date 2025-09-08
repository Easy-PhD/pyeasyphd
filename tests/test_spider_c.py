import os
from typing import Any, Dict

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import CheckDeleteFormatMoveSpideredBibs

if __name__ == "__main__":
    options: Dict[str, Any] = {}
    options = {
        # url
        "check_duplicate_url": False,
        "delete_duplicate_url": False,
        # bib
        "format_bib": False,
        "write_bib": False,
        "check_duplicate_bib": False,
        "delete_duplicate_bib": False,
        "move_bib": False,
        # include and exclude
        "include_publisher_list": [],
        "include_abbr_list": [],
        "exclude_publisher_list": [],
        "exclude_abbr_list": [],
    }

    options["path_config"] = local_paths["path_config"]
    path_storage = os.path.join(local_paths["path_spidering_bibs"], "spider_c")
    path_shutil = os.path.join(local_paths["path_spidered_bibs"], "Conferences")

    CheckDeleteFormatMoveSpideredBibs(path_storage, path_shutil, options).check_delete_format_move()
    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
