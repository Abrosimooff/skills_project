from __future__ import unicode_literals, absolute_import, division, print_function

import os
import sys

DEBUG = True

home = os.path.join(os.path.expanduser("~"), "work", "skills_project")
sys.path.append(os.path.join(home, "colors_app"))
sys.path.append(os.path.join(home, "skills"))

INSTALLED_APPS_LOCAL = [
    'colors_app'
]
