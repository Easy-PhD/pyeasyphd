import os

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import PaperLinksGenerator, generate_from_bibs_and_write

if __name__ == "__main__":
    options = {}
    options = {
        "include_publisher_list": [],
        "include_abbr_list": [],
        "exclude_publisher_list": [],
        "exclude_abbr_list": [],
        # for IEEE
        "early_access": False,
    }
    options["path_config"] = local_paths["path_config"]

    # Customized by USERS
    path_weekly_docs = ""
    path_yearly_docs = ""

    cj = "Journals"

    for gc in ["generate_data", "combine_data"]:

        if options.get("early_access", False):
            path_storage = os.path.join(local_paths["path_spidering_bibs"], "spider_j_e")
            output_basename = os.path.join("data", "Weekly")
            path_output = os.path.expanduser(os.path.join(local_paths["path_output"], output_basename, cj))
            # "current_month"
            for flag in []:
                generate_from_bibs_and_write(
                    path_storage, path_output, output_basename, cj, gc, "current_year", flag, options
                )

            # "all_years"
            for year in []:
                generate_from_bibs_and_write(
                    path_storage, path_output, output_basename, cj, gc, year, "all_months", options
                )
        else:
            path_storage = os.path.join(local_paths["path_spidering_bibs"], "spider_j")
            output_basename = os.path.join("data", "Weekly")
            path_output = os.path.expanduser(os.path.join(local_paths["path_output"], output_basename, cj))
            # "current_issue", "current_month", "all_months"
            for flag in []:
                generate_from_bibs_and_write(
                    path_storage, path_output, output_basename, cj, gc, "current_year", flag, options
                )

            path_storage = os.path.join(local_paths["path_spidered_bibs"], "Journals")
            output_basename = os.path.join("data", "Yearly")
            path_output = os.path.expanduser(os.path.join(local_paths["path_output"], output_basename, cj))
            # "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"
            for year in []:
                generate_from_bibs_and_write(
                    path_storage, path_output, output_basename, cj, gc, year, "all_months", options
                )

    for keywords_category_name in ["", "S", "Y"]:
        output_basename = os.path.join("data", "Weekly")
        generator = PaperLinksGenerator(local_paths["path_json"], path_weekly_docs, keywords_category_name)
        generator.generate_ieee_early_access_links(output_basename)
        generator.generate_weekly_links(output_basename)
        generator.generate_keywords_links_monthly(cj, output_basename)

        output_basename = os.path.join("data", "Yearly")
        generator = PaperLinksGenerator(local_paths["path_json"], path_yearly_docs, keywords_category_name)
        generator.generate_yearly_links(cj, output_basename)
        generator.generate_keywords_links_yearly(cj, output_basename)

    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
