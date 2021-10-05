import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union
from urllib.error import HTTPError
from urllib.request import urlopen

__version__ = "0.1.1"

# types
TemplateType = Dict[str, Union[List[str], Dict[str, str]]]


TEMPLATES_URL = "https://raw.githubusercontent.com/Adwaith-Rajesh/any-template/master/templates/"
TEMPLATE_LIST_URL = "https://api.github.com/repos/Adwaith-Rajesh/any-template/contents/templates"


example_use = """
    Example use:

        anytemp use python-fast-api
        anytemp use python --license MIT
        anytemp use python --git
        anytemp ls
        anytemp ls -c python
"""

license_choices = {
    'agpl-3.0': 'https://api.github.com/licenses/agpl-3.0',
    'apache-2.0': 'https://api.github.com/licenses/apache-2.0',
    'bsd-2-clause': 'https://api.github.com/licenses/bsd-2-clause',
    'bsd-3-clause': 'https://api.github.com/licenses/bsd-3-clause',
    'bsl-1.0': 'https://api.github.com/licenses/bsl-1.0',
    'cc0-1.0': 'https://api.github.com/licenses/cc0-1.0',
    'epl-2.0': 'https://api.github.com/licenses/epl-2.0',
    'gpl-2.0': 'https://api.github.com/licenses/gpl-2.0',
    'gpl-3.0': 'https://api.github.com/licenses/gpl-3.0',
    'lgpl-2.1': 'https://api.github.com/licenses/lgpl-2.1',
    'mit': 'https://api.github.com/licenses/mit',
    'mpl-2.0': 'https://api.github.com/licenses/mpl-2.0',
    'unlicense': 'https://api.github.com/licenses/unlicense'
}


def get_template(template_name: str) -> Union[TemplateType, None]:
    template_name = template_name.replace(".json", "")
    full_url = f"{TEMPLATES_URL}{template_name}.json"

    try:
        response = urlopen(full_url)

    except HTTPError:
        return None

    if response.status == 200:
        data = json.loads(response.read())
        return data

    return None


def get_all_templates() -> List[str]:
    templates = []
    try:
        response = urlopen(TEMPLATE_LIST_URL)
        if response.status == 200:
            data = json.loads(response.read())

            for d in data:
                templates.append(d["name"].replace(".json", ""))
            return templates

        else:
            return []

    except (HTTPError, json.decoder.JSONDecodeError):
        return []


def build_template(template: TemplateType) -> None:

    def create_file(filename: str) -> None:
        Path(filename).touch()

    def create_file_with_contents(filename: str, content: str) -> None:
        with open(filename, "w") as f:
            f.write(content)

    def get_remote_file_content(url: str) -> str:
        try:
            response = urlopen(url)
            if response.status == 200:
                return response.read().decode("utf-8")
            else:
                return ""

        except HTTPError:
            return ""

    def get_license(url: str) -> str:
        try:
            response = urlopen(url)
            if response.status == 200:
                return json.loads(response.read())["body"]
            else:
                return ""

        except (HTTPError, json.decoder.JSONDecodeError):
            return ""

    for folder in template["folders"]:
        Path(folder).mkdir(parents=True, exist_ok=True)

    for filename in template["files"]:
        create_file(filename)

    if isinstance(template["files_with_contents"], dict):
        for filename, url in template["files_with_contents"].items():
            if not filename == "LICENSE":
                create_file_with_contents(
                    filename, get_remote_file_content(url))
            else:
                create_file_with_contents(filename, get_license(url))


def main(argv: Optional[Sequence[str]] = None) -> int:

    parser = argparse.ArgumentParser(
        description="CLI tool to get you started with any programming project",
        epilog=example_use,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="commands")
    parser.add_argument("-v", action="store_true",
                        help="Info about any-template")

    # the use command
    use = sub.add_parser(
        "use", help="Allows the user to use a template to build a project")
    use.add_argument("template", type=str, help="The template to use")
    use.add_argument("-l", "--license",
                     help="The license to use for the project.",
                     default="mit", type=str)
    use.add_argument("--git",
                     help="Initialize a git repo",
                     action="store_true")

    ls = sub.add_parser(
        "ls", help="List all the available templates."
    )
    ls.add_argument("-c", "--contains",
                    help="Only show templates that contains a specific word",
                    type=str
                    )

    args = parser.parse_args(argv)

    if not args.commands and args.v:
        print(
            f"any-template: {__version__} \n\nGithub: https://github.com/Adwaith-Rajesh/any-template")
        return 0

    if args.commands == "use":
        template = get_template(args.template)

        if template:

            if args.license.lower() not in list(license_choices):
                print(
                    f"Unknown license {args.license!r}. Using MIT instead. Must be any of.")
                for name in list(license_choices):
                    print(name)
                setattr(args, "license", "mit")

            if isinstance(template["files_with_contents"], dict):
                template["files_with_contents"]["LICENSE"] = license_choices[args.license.lower()]
            build_template(template)

            if args.git:
                if not Path(".git").is_dir():
                    ec = os.system("git init")
                    return ec

                else:
                    print("git is already initialized.", file=sys.stderr)
                    return 2

            return 0

        else:
            print("Template does not exits.\nUse 'anytemp ls' to list all the available templates", file=sys.stderr)
            return 1

    if args.commands == "ls":
        templates = get_all_templates()
        if args.contains:
            templates = list(filter(lambda x: args.contains in x, templates))

        for template_name in templates:
            print(template_name)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
