import os
from typing import Any, Dict

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import compare_bibs_with_zotero

if __name__ == "__main__":
    options: Dict[str, Any] = {}
    options["path_config"] = local_paths["path_config"]

    path_output = os.path.join(local_paths["path_output"], "comparision_new")

    zotero_bib = os.path.join(local_paths["path_output"], "comparision_old/zotero.bib")
    download_bib = os.path.join(local_paths["path_output"], "comparision_old/download.bib")

    compare_bibs_with_zotero(zotero_bib, download_bib, path_output, options)
    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
