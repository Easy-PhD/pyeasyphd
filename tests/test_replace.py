import os
from typing import Any, Dict

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import replace_to_standard_cite_keys

if __name__ == "__main__":
    options: Dict[str, Any] = {}
    options["path_config"] = local_paths["path_config"]

    path_output = os.path.join(local_paths["path_output"], "replacement_new")

    full_tex = os.path.join(local_paths["path_output"], "replacement_old/old.tex")
    full_bib = os.path.join(local_paths["path_output"], "replacement_old/old.bib")

    replace_to_standard_cite_keys(full_tex, full_bib, path_output, options)
    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
