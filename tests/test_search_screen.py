import os
from typing import Any, Dict

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import Searchkeywords


def generate_options(options: Dict[str, Any] = {}):
    options["print_on_screen"] = True

    options["search_year_list"] = ['2017']
    options["include_publisher_list"] = []
    options["include_abbr_list"] = ["NeurIPS"]
    options["exclude_publisher_list"] = []
    options["exclude_abbr_list"] = []

    keywords_type = "Temp"
    keywords_list_list = [
        ["Attention is all you need"]
    ]

    options["keywords_dict"] = {keywords_type: keywords_list_list}
    options["keywords_type_list"] = [keywords_type]
    return options


if __name__ == "__main__":
    options = generate_options()
    options["path_config"] = local_paths["path_config"]

    for i, j in zip(["Journals", "Conferences"], ["Journals", "Conferences"]):
        path_storage = os.path.join(local_paths["path_spidered_bibs"], f"{i}")
        path_output = os.path.join(local_paths["path_output"], "Search_spidered_bib", j)
        Searchkeywords(path_storage, path_output, options).run()

    for i, j in zip(["spider_j", "spider_j_e"], ["spider_j", "spider_j_e"]):
        path_storage = os.path.join(local_paths["path_spidering_bibs"], f"{i}")
        path_output = os.path.join(local_paths["path_output"], "Search_spidering_bib", j)
        Searchkeywords(path_storage, path_output, options).run()

    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
