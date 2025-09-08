import os
from typing import Any, Dict

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import compare_bibs_with_local

if __name__ == "__main__":
    options: Dict[str, Any] = {
        "path_config": local_paths["path_config"],
        "include_publisher_list": [],
        "include_abbr_list": [],
        "exclude_publisher_list": [],
        "exclude_abbr_list": [],
        # for IEEE
        "include_early_access": True,
    }

    path_spidered_bibs = local_paths["path_spidered_bibs"]
    path_spidering_bibs = local_paths["path_spidering_bibs"]
    path_output = os.path.join(local_paths["path_output"], "comparision_new")

    path_storage = os.path.join(local_paths["path_output"], "comparision_old")

    compare_bibs_with_local(path_storage, path_spidered_bibs, path_spidering_bibs, path_output, options)
    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
