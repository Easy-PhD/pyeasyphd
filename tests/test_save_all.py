import os
from typing import Any, Dict

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import (
    format_entries_for_abbr_zotero_save,
    generate_standard_publisher_abbr_options_dict,
    generate_statistic_information,
)


class FormatAllConferenceOrJournalPapers(object):
    def __init__(self, path_storage: str, path_output: str) -> None:
        self.path_storage = path_storage
        self.path_output = path_output

    def run(self, options: Dict[str, Any]) -> None:
        publisher_abbr_dict = generate_standard_publisher_abbr_options_dict(self.path_storage, options)
        for publisher in publisher_abbr_dict:
            for abbr_standard in publisher_abbr_dict[publisher]:
                new_options = publisher_abbr_dict[publisher][abbr_standard]
                path_storage = os.path.join(self.path_storage, f"{publisher.lower()}/{abbr_standard}")
                path_output = os.path.join(self.path_output, f"{publisher.lower()}/{abbr_standard}")

                print(f"Format and save `{publisher}-{abbr_standard}` ...")
                format_entries_for_abbr_zotero_save(abbr_standard, path_output, path_storage, options=new_options)
                generate_statistic_information(path_output)
                print("Successful.\n")


if __name__ == "__main__":
    options: Dict[str, Any] = {}
    options = {
        "include_publisher_list": [],
        "include_abbr_list": [],
        "exclude_publisher_list": [],
        "exclude_abbr_list": [],
    }
    options["path_config"] = local_paths["path_config"]

    for i, j in zip(["Journals", "Conferences"], ["Journals", "Conferences"]):
        path_storage = os.path.join(local_paths["path_spidered_bibs"], f'{i}')
        path_output = os.path.join(local_paths["path_output"], f'Save_all/{j}')
        FormatAllConferenceOrJournalPapers(path_storage, path_output).run(options)
    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
