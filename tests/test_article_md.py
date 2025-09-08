import os

from local_paths import local_paths
from pyadvtools import delete_python_cache

from pyeasyphd.tools import PyRunBibMdTex

if __name__ == "__main__":
    options = {
        "path_config": local_paths["path_config"],

        # figure options
        "shutil_figures": False,
        "figure_folder_name": "fig",  # "" or "figs" or "main"

        # bib options
        "maximum_authors_for_abbr": 1,  # 0, 1, 2, ...
        "add_link_to_fields_for_abbr": None,  # None, or ["title", "journal", "booktitle"]
        "abbr_index_article_for_abbr": 2,  # 0, 1, 2
        "abbr_index_inproceedings_for_abbr": 2,  # 0, 1, 2
        "bib_folder_name": "bib",  # "" or "bib" or "main"
        "add_index_to_entries": True,
        "bib_for_abbr_name": "abbr.bib",
        "bib_for_zotero_name": "zotero.bib",
        "bib_for_save_name": "save.bib",
        "display_google_connected_scite": ["google", "connected", "scite"],
        "delete_original_bib_in_output_folder": False,

        # tex options
        "final_output_main_tex_name": "main.tex",
        "generate_tex": False,
        "handly_preamble": False,
        "tex_folder_name": "tex",  # "" or "tex" or "main"
        "run_latex": False,
        "delete_run_latex_cache": False,
        "delete_original_tex_in_output_folder": False,

        # md options
        "final_output_main_md_name": "main.md",
        "md_folder_name": "md",  # "" or "md" or "main"
        "delete_temp_generate_md": True,
        "add_reference_in_md": True,
        "add_bib_in_md": False,
        "replace_cite_to_fullcite_in_md": True,
        "replace_by_basic_beauty_complex_in_md": "beauty",
        "display_basic_beauty_complex_references_in_md": "beauty",
        "delete_original_md_in_output_folder": False,

        # html options
        "generate_html": False
    }

    path_notes, path_output = local_paths["path_notes"], local_paths["path_output"]

    file_list = ["note_md/test.md"]
    file_list = [os.path.join(path_notes, f) for f in file_list]
    PyRunBibMdTex(path_output, ".md", "paper", options).run_files(file_list)
    delete_python_cache(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
