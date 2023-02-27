# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import pathlib


def fetch_version(max_folders_up: int = 3) -> tuple[str, str]:
    """
    Fetches the version number for the pyproject.toml
    folder no more than 2 up.

    Args:
        max_folders_up (int): Max number of folders up to search.

    Returns:
        tuple[str, str]: Release and Version number for project,
                         using the semantic version style.
                         E.g. "0.1.1", "0.1"
    """
    ret_release: str = ">0.2.0"
    try:
        for idx in range(max_folders_up):
            path = pathlib.Path("../" * idx + "pyproject.toml")
            if path.is_file():
                break
        else:
            raise FileNotFoundError("pyproject.toml not found")
        pyproject_toml = path.resolve()
        with open(pyproject_toml, "r") as fin:
            for line in fin.readlines():
                if line.startswith("version"):
                    ret_release = line.split('"')[1]
    except FileNotFoundError:
        raise
    ret_version: str = ret_release.rpartition(".")[0]
    return ret_release, ret_version


project = "Town Clock"
copyright = "2023, Zack Hankin <zthankin@gmail.com>"
author = "Zack Hankin <zthankin@gmail.com>"
release, _ = fetch_version()
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
    "sphinx.ext.viewcode",
    "sphinx.ext.duration",
    "sphinx.ext.coverage",
    "sphinx_rtd_theme",
    "myst_parser",
]

add_module_names = False

templates_path = ["_templates"]
exclude_patterns = []

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# -- Napoleon settings -------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#module-sphinx.ext.napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
