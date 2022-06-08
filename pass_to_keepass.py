#!/usr/bin/env python3
# encoding: utf-8

"""
Export your pass database to keepass
1. Define, wihtin your pass database a 'keepass' password containing the desired keypass
   password
2. call pass_to_keepass.py
3. open the keepass.kdbx
"""

import logging
import os
import subprocess
from argparse import ArgumentParser
from collections import namedtuple
from pathlib import Path

import pykeepass
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

# the path of the PASS database
def export_passwords(to_file: str, kp_password: str, max_number: int = None):
    """Export the passwords."""
    logging.info(f"Creating database {to_file} {max_number=}")
    db = pykeepass.create_database(to_file, kp_password)
    pass_base_path = Path(
        os.environ.get("PASSWORD_STORE_DIR", "~/.password-store")
    ).expanduser()

    # list all the passwords found in pass database
    export_passwords = list(pass_base_path.rglob("*.gpg"))
    if max_number:
        export_passwords = export_passwords[:max_number]

    # we will add all password in the root group
    group = db.root_group

    # export all password - using tqdm to print a progressbar
    for full_password_path in tqdm(export_passwords):
        pass_path = full_password_path.relative_to(pass_base_path)
        pass_path_str = str(pass_path).replace(".gpg", "")

        # use the first item of pass as SITE URL, adding a https:// scheme
        base_path = pass_path.parts[0]
        username = pass_path.parts[-1].replace(".gpg", "")

        url = f"https://{base_path}" if "." in base_path else base_path

        # retrieve the password from path
        password, notes = get_pass(pass_path_str)

        db.add_entry(
            destination_group=group,
            title=pass_path_str.removeprefix("/"),
            url=url,
            username=username,
            password=password,
            notes=notes,
        )

    db.save()
    print(f"Saved to file {to_file}")


PassInfo = namedtuple("PassInfo", ["password", "notes"])


def get_pass(pass_path: str) -> PassInfo:
    """Get password and notes from pass."""
    lines = subprocess.check_output(["pass", pass_path]).decode().splitlines()
    password = lines[0]
    notes = "\n".join(lines[1:])
    return PassInfo(password, notes)


if __name__ == "__main__":

    parser = ArgumentParser("pass_to_keepass")
    parser.add_argument(
        "-o",
        "--output",
        help="the KEEPASS database to generate, 'keepass.kdbx' by default",
        default="keepass.kdbx",
        required=False,
    )
    parser.add_argument(
        "-p",
        "--password",
        help="The keepass password name in the pass database, 'keepass' by default",
        default="keepass",
        required=False,
    )
    parser.add_argument(
        "-n",
        "--number",
        help="The max number of password to export",
        required=False,
    )

    args = parser.parse_args()
    number = int(args.number) if args.number else None
    export_passwords(args.output, get_pass(args.password).password, max_number=number)
