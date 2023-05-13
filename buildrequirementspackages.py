import os
import requests

API_URL = 'https://pypi.openknowit.com/pypi-packages'

# Generate requirements.txt file if it does not exist
if not os.path.isfile('requirements.txt'):
    os.system('pip freeze > requirements.txt')

# Read requirements.txt file and send package data to API
with open('requirements.txt') as f:
    for line in f:
        # Remove whitespace and comments
        line = line.strip()
        if line.startswith('#'):
            continue

        # Split package name and version specifier
        parts = line.split('==')
        package_name = parts[0]
        version_specifier = parts[1] if len(parts) > 1 else None

        # Send package data to API
        package_data = {
            'name': package_name,
            'version': version_specifier,
            'seuppy': False,
            'setupcfg': False,
            'prettysetuppy': False,
            'pyprojecttoml': False,
            'sourcedownloaded': False,
            'sourceupacked': False,
            'specfile': "",
            'specfilecreated': False,
            'rpmbuild': False,
            'rpmfilepublished': False,
            'debbuild': False
        }
        response = requests.post(API_URL, json=package_data)
        if response.status_code == 200:
            print(f'Registered package: {package_name}')
        else:
            print(f'Error registering package {package_name}: {response.text}')
