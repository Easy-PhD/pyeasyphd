import os
from typing import Any, Dict

from pyadvtools import read_list
from pybibtexer.main import BasicInput as BasicInputInPyBibtexer


class BasicInput(BasicInputInPyBibtexer):
    """Basic input.

    Args:
        options (Dict[str, Any]): Options.

    Attributes:
        full_json_c (str):
        full_json_j (str):
        full_csl_style_pandoc (str): Full path to csl style for pandoc.
        full_tex_article_template_pandoc (str): Full path to tex article template for pandoc.
        full_tex_beamer_template_pandoc (str): Full path to tex beamer template for pandoc.
        article_template_tex (List[str]): Article template for LaTex.

        article_template_header_tex (List[str]): Article template header for LaTex.
        article_template_tail_tex (List[str]): Article template tail for LaTex.
        beamer_template_header_tex (List[str]): Beamer template header for LaTex.
        beamer_template_tail_tex (List[str]): Beamer template tail for LaTex.
        math_commands_tex (List[str]): Tex math commands for LaTex.
        usepackages_tex (List[str]): Tex usepackages for LaTex.
        handly_preamble (bool): Handly preamble.

        options (Dict[str, Any]): Options.
    """

    def __init__(self, options: Dict[str, Any]) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self._path_templates = os.path.join(os.path.dirname(current_dir), "data", "Templates")

        full_json_c = os.path.join(self._path_templates, "AbbrFull", "conferences.json")
        full_json_j = os.path.join(self._path_templates, "AbbrFull", "journals.json")

        _full_json_c = options.get("full_json_c")
        if isinstance(_full_json_c, "str"):
            full_json_c = _full_json_c
        _full_json_j = options.get("full_json_j")
        if isinstance(_full_json_j, "str"):
            full_json_j = _full_json_j

        super().__init__(full_json_c, full_json_j, options)

        # main
        self._initialize_pandoc_md_to(options)
        self._initialize_python_run_tex(options)

        self.options = options

    # main
    def _initialize_pandoc_md_to(self, options: Dict[str, Any]) -> None:
        csl_name = options.get("csl_name", "apa-no-ampersand")
        if not isinstance(csl_name, str):
            csl_name = "apa-no-ampersand"
        self.full_csl_style_pandoc = os.path.join(self._path_templates, "CSL", f"{csl_name}.csl")
        if not os.path.exists(self.full_csl_style_pandoc):
            self.full_csl_style_pandoc = os.path.join(self._path_templates, "CSL", "apa-no-ampersand.csl")

        self.full_tex_article_template_pandoc = os.path.join(self._path_templates, "TEX", "eisvogel.latex")
        self.full_tex_beamer_template_pandoc = os.path.join(self._path_templates, "TEX", "eisvogel.beamer")

        self.article_template_tex = self._try_read_list("TEX", "Article.tex")

    def _initialize_python_run_tex(self, options: Dict[str, Any]) -> None:
        self.article_template_header_tex = self._try_read_list("TEX", "Article_Header.tex")
        self.article_template_tail_tex = self._try_read_list("TEX", "Article_Tail.tex")
        self.beamer_template_header_tex = self._try_read_list("TEX", "Beamer_Header.tex")
        self.beamer_template_tail_tex = self._try_read_list("TEX", "Beamer_Tail.tex")
        self.math_commands_tex = self._try_read_list("TEX", "math_commands.tex")
        self.usepackages_tex = self._try_read_list("TEX", "Style.tex")

        # handly preamble
        self.handly_preamble = options.get("handly_preamble", False)
        if self.handly_preamble:
            self.article_template_header_tex, self.article_template_tail_tex = [], []
            self.beamer_template_header_tex, self.beamer_template_tail_tex = [], []
            self.math_commands_tex, self.usepackages_tex = [], []

    def _try_read_list(self, folder_name: str, file_name: str):
        path_file = os.path.join(self._path_templates, folder_name, file_name)

        try:
            data_list = read_list(path_file)
        except Exception as e:
            print(e)
            data_list = []
        return data_list
