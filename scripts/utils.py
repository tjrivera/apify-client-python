import pathlib
import re

PACKAGE_NAME = 'apify_client'
REPO_ROOT = pathlib.Path(__file__).parent.resolve() / '..'
PYPROJECT_TOML_FILE_PATH = REPO_ROOT / 'pyproject.toml'


# Load the current version number from pyproject.toml
# It is on a line in the format `version = "1.2.3"`
def get_current_package_version() -> str:
    with open(PYPROJECT_TOML_FILE_PATH, 'r') as pyproject_toml_file:
        for line in pyproject_toml_file:
            if line.startswith('version = '):
                delim = '"' if '"' in line else "'"
                version = line.split(delim)[1]
                return version
        else:
            raise RuntimeError('Unable to find version string.')


# Write the given version number from pyproject.toml
# It replaces the version number on the line with the format `version = "1.2.3"`
def set_current_package_version(version: str) -> None:
    with open(PYPROJECT_TOML_FILE_PATH, 'r+') as pyproject_toml_file:
        updated_pyproject_toml_file_lines = []
        version_string_found = False
        for line in pyproject_toml_file:
            if line.startswith('version = '):
                version_string_found = True
                line = f'version = "{version}"'
            updated_pyproject_toml_file_lines.append(line)

        if not version_string_found:
            raise RuntimeError('Unable to find version string.')

        pyproject_toml_file.seek(0)
        pyproject_toml_file.write('\n'.join(updated_pyproject_toml_file_lines))
        pyproject_toml_file.truncate()


# Generate convert a docstring from a sync resource client method
# into a doctring for its async resource client analogue
def sync_to_async_docstring(docstring: str) -> str:
    substitutions = [(r'Client', r'ClientAsync')]
    res = docstring
    for (pattern, replacement) in substitutions:
        res = re.sub(pattern, replacement, res, flags=re.M)
    return res
