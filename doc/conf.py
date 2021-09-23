# -*- coding: utf-8 -*-

from json import loads
from pathlib import Path

import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- General configuration ------------------------------------------------

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

templates_path = ["_templates"]

source_suffix = [".rst"]

master_doc = "index"

project = u"pyHDLParser"
copyright = u"2017, Kevin Thibedeau and contributors"
author = u"Kevin Thibedeau"


def get_package_version(verfile):
    """Scan the script for the version string"""
    version = None
    with open(verfile) as fh:
        try:
            version = [
                line.split("=")[1].strip().strip("'")
                for line in fh
                if line.startswith("__version__")
            ][0]
        except IndexError:
            pass
    return version


version = get_package_version("../hdlparse/minilexer.py")
release = version

language = None

exclude_patterns = ["_build", "_theme", "Thumbs.db", ".DS_Store"]

pygments_style = "stata-dark"

todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

html_theme_path = ["."]
html_theme = "_theme"

html_theme_options = {
    "logo_only": False,
    "home_breadcrumbs": True,
    "vcs_pageview_mode": "blob",
}

html_context = {}

ctx = Path(__file__).resolve().parent / "context.json"
if ctx.is_file():
    html_context.update(loads(ctx.open("r").read()))

#html_static_path = ["_static"]


# -- Options for HTMLHelp output ------------------------------------------

htmlhelp_basename = "pyHDLParserDoc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {}

latex_documents = [
    (
        master_doc,
        "pyHDLParser.tex",
        u"pyHDLParser Documentation",
        u"Kevin Thibedeau",
        "manual",
    ),
]


# -- Options for manual page output ---------------------------------------

man_pages = [(master_doc, "hdlparse", u"pyHDLParser Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (
        master_doc,
        "pyHDLParser",
        u"pyHDLParser Documentation",
        author,
        "pyHDLParser",
        "One line description of project.",
        "Miscellaneous",
    ),
]
