import os
from typing import Any, Dict

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import format_entries_for_abbr_zotero_save

if __name__ == '__main__':
    options: Dict[str, Any] = {}

    # "abbr", "zotero", or "save"
    choose_abbr_zotero_save = "save"
    j_conf_abbr = "TEVC"
    combine_year_length = 1

    options["default_additional_field_list"] = []
    options["choose_abbr_zotero_save"] = choose_abbr_zotero_save

    # "save"
    options["delete_fields_list_for_save"] = [
        # "article-number", "author-email", "book-group-author", "doc-delivery-number", "eissn",
        # "funding-acknowledgement", "funding-text",
        # "isbn", "issn", "journal-iso", "keywords-plus", "language",
        # "note", "number-of-cited-references", "orcid-numbers",
        # "research-areas", "researcherid-numbers",
        # "times-cited", "type",
        # "unique-id", "usage-count-last-180-days", "usage-count-since-2013",
        # "web-of-science-categories", "web-of-science-index",

        # "address", "affiliation", "affiliations", "editor",
        # "keywords", "organization", "publisher", "series",
    ]

    # "zotero"
    options["delete_fields_list_for_zotero"] = []

    options["path_config"] = local_paths["path_config"]
    path_storage = os.path.join(local_paths["path_output"], "abbr_zotero_save")
    path_output = os.path.join(local_paths["path_output"], choose_abbr_zotero_save)

    format_entries_for_abbr_zotero_save(j_conf_abbr, path_output, path_storage, combine_year_length, options=options)
    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
