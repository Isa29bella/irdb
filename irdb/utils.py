import os
from os import path as pth
from pathlib import Path
import yaml

from irdb.system_dict import SystemDict

PKG_DIR = Path(__file__).parent.parent


def get_packages():
    """
    Returns a dictionary with all packages in the IRDB

    Returns
    -------
    pkgs : dict
        {"packge_name" : "path_to_package"}
    """
    # TODO: update docstring for generator
    for pkg_path in PKG_DIR.iterdir():
        if (pkg_path / f"{pkg_path.name}.yaml").exists():
            yield pkg_path.name, pkg_path


def recursive_filename_search(entry):
    """
    Search through a yaml dict looking for the keyword "filename"

    Parameters
    ----------
    entry : dict
        A yaml nested dictionary

    Returns
    -------
    fnames : list
        List of all filenames found

    """
    fnames = []
    if isinstance(entry, list):
        for item in entry:
            fnames.extend(recursive_filename_search(item))

    if isinstance(entry, dict):
        for key, value in entry.items():
            if key.lower() in {"filename", "file_name"}:
                fnames.append(value)
            elif isinstance(value, (dict, list)):
                fnames.extend(recursive_filename_search(value))

    return fnames
