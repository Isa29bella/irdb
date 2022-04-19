#!/usr/bin/env python3
"""IRDB"""

from distutils.core import setup
import os
from os import path as pth

# Version number
with open('irdb/version.py') as f:
    __version__ = f.readline().split("'")[1]


def create_manifest():
    pkgs_list = [pkg for pkg in os.listdir("./") if \
                 pth.isdir(pkg) and pth.exists(pth.join(pkg, f"{pkg}.yaml"))]
    with open("MANIFEST.in", "w") as f:
        for pkg_name in pkgs_list:
            f.write(f"include {pkg_name}/*\n")
            print(f"Including {pkg_name}")


def setup_package():
    setup(name = 'IRDB',
          version = __version__,
          description = "Instrument package database",
          author = "Kieran Leschinski",
          author_email = "kieran.leschinski@unive.ac.at",
          url = "http://homepage.univie.ac.at/kieran.leschinski/",
          packages = ["irdb/tests"],
          )


if __name__ == '__main__':
    create_manifest()
    setup_package()
