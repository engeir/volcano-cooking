"""Functions used across scripts in the helper_scripts module."""

import os
import sys
from typing import Optional


def find_original(filename: Optional[str] = None) -> str:
    """Find the original .nc file with volcanic forcing.

    If nothing is specified, the function assumes the file name is
        `volcan-eesm_global_2015_so2-emissions-database_v1.0.nc`
    Optionally, the file name can be specified (it is still assumed it can be found in
    data/originals/).

    Parameters
    ----------
    filename: str (optional)
        Name of the file inside the originals directory you want to look at

    Returns
    -------
    str
        The path and name of the original forcing file
    """
    orig_dir = "data/originals/"
    if not os.path.isdir(orig_dir):
        os.makedirs(orig_dir)
    if filename is None:
        original_file = (
            "data/originals/volcan-eesm_global_2015_so2-emissions-database_v1.0.nc"
        )
    else:
        if filename[0] == "/":
            filename = filename[1:]
        if ".nc" not in filename:
            filename += ".nc"
        original_file = orig_dir + filename
    if not os.path.isfile(original_file):
        sys.exit(f"Can't find file {original_file}")

    return original_file


def find_last_output(ext: str) -> str:
    """Search in the output folder for a given file type and return last found file.

    Parameters
    ----------
    ext: str
            The file ending

    Returns
    -------
    str
        The path and name of the last saved .nc file

    Raises
    ------
    ValueError
        If the extension provided is not recognised
    """
    if ext[0] != "." and "." in ext:
        raise ValueError(
            f"{ext} is not a valid extension. Use '.npz', 'npz', '.nc' or 'nc'."
        )
    elif ext[0] != ".":
        ext = f".{ext}"
    synth_dir = "data/output"
    if not os.path.isdir(synth_dir):
        os.makedirs(synth_dir)
    synth_files = [
        f
        for f in os.listdir(synth_dir)
        if os.path.isfile(os.path.join(synth_dir, f)) and ext in f
    ]
    if len(synth_files) == 0:
        sys.exit("No output files found.")
    synth_files.sort()
    file = os.path.join(synth_dir, synth_files[-1])

    return file


def find_file(file: str) -> str:
    """Check if the file is found.

    Parameters
    ----------
    file: str
        Full path (absolute or relative to where the function i called) and file name of a
        custom file to be used.

    Returns
    -------
    str
        The same str that was sent in

    Raises
    ------
    ValueError
        If the file cannot be found in the path where the python interpreter is run a
        ValueError is raised.
    """
    if os.path.isfile(file):
        return file
    else:
        raise ValueError(f"Cannot find {file} =  in path {os.getcwd()}]")
