import os
from typing import Any, Dict

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import PaperLinksGenerator, generate_from_bibs_and_write

if __name__ == "__main__":
    options: Dict[str, Any] = {}
    options = {
        "include_publisher_list": [],
        "include_abbr_list": [],
        "exclude_publisher_list": [],
        "exclude_abbr_list": [],
    }
    options["path_config"] = local_paths["path_config"]

    # Customized by USERS
    path_yearly_docs = ""

    path_storage = os.path.join(local_paths["path_spidered_bibs"], "Conferences")

    output_basename = os.path.join("data", "Yearly")
    cj = "Conferences"
    path_output = os.path.expanduser(os.path.join(local_paths["path_output"], output_basename, cj))

    for gc in ["generate_data", "combine_data"]:

        # "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"
        for year_flag in []:
            generate_from_bibs_and_write(
                path_storage, path_output, output_basename, cj, gc, year_flag, "all_months", options
            )

    for keywords_category_name in ["", "S", "Y"]:
        generator = PaperLinksGenerator(local_paths["path_json"], path_yearly_docs, keywords_category_name)
        generator.generate_yearly_links(cj, output_basename)
        generator.generate_keywords_links_yearly(cj, output_basename)

    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
