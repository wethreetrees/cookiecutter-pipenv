import re
import sys
import subprocess
import json


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.project_slug }}'
github_username = '{{ cookiecutter.github_username }}'

if not re.match(MODULE_REGEX, module_name):
    print(('ERROR: The project slug (%s) is not a valid Python module name. Please do not use'
           ' a - and use _ instead' % module_name))

    # Exit to cancel project
    sys.exit(1)

try:
    hubCommand = "hub api user/repos"
    process = subprocess.Popen(hubCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    repos = json.loads(output)
    thisRepo = [repo for repo in repos if repo['full_name'] == f"{github_username}/{module_name}"]
    if thisRepo:
        print(('ERROR: The repository (%s) already exists. Please select a new project name.' % f"{github_username}/{module_name}"))

        # Exit to cancel project
        sys.exit(1)
except FileNotFoundError:
    print('ERROR: github hub not installed. See site for further info: https://github.com/github/hub')

    # Exit to cancel project
    sys.exit(1)
