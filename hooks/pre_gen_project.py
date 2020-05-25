import re
import requests
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.project_slug }}'
github_username = '{{ cookiecutter.github_username }}'

if not re.match(MODULE_REGEX, module_name):
    print(('ERROR: The project slug (%s) is not a valid Python module name. Please do not use'
           ' a - and use _ instead' % module_name))

    # Exit to cancel project
    sys.exit(1)

response = requests.get(f"https://api.github.com/repos/{github_username}/{module_name}")

try:
    response.raise_for_status()
except requests.exceptions.HTTPError:
    print(('ERROR: The repository (%s) already exists. Please select a new project name.' % f"{github_username}/{module_name}"))

    sys.exit(1)
