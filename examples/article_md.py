from pyeasyphd.scripts.run_article_md import run_article_md_daily_notes

if __name__ == "__main__":
    path_conf_j_jsons = ""
    zotero_bib = ""
    path_input_file = ""
    path_output_file = ""
    options = {}

    input_file_names = ["Introduction.md", "Algorithms.md", "Metrics.md", "Applications.md"]

    run_article_md_daily_notes(
        path_input_file, input_file_names, path_output_file, zotero_bib, path_conf_j_jsons, options
    )
