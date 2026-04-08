project = "Mutation Game"
copyright = "2026"
author = ""

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 3,
}
html_static_path = ["_static"]

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "src")))
