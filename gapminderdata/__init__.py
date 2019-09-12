import logging
import os
import re
import shutil
import tempfile
import zipfile
from functools import wraps, lru_cache
from pathlib import Path
from typing import Iterable, List, Union

import pandas
import requests

_DEFAULT_CACHE_DIR = Path.home() / ".python-gapminderdata"

CACHE_DIR: Path = Path(os.environ.get("GAPMINDER_DATA_CACHE", _DEFAULT_CACHE_DIR))
SOURCE_URL: str = "https://github.com/open-numbers/ddf--gapminder--systema_globalis/archive/master.zip"


def download_data(destination: Union[Path, str], overwrite: bool = False):
    """Download and extract data to any directory."""
    destination = Path(destination)
    if destination.is_dir():
        if overwrite:
            raise RuntimeError("Data already downloaded.")

    try:
        temp_dir = tempfile.mkdtemp()
        download_path = os.path.join(temp_dir, "data.zip")

        response = requests.get(SOURCE_URL)
        if response.status_code == 200:
            with open(download_path, "wb") as download_file:
                download_file.write(response.content)
        else:
            raise RuntimeError(f"Cannot download data from {SOURCE_URL}.")

        if destination.is_dir():
            shutil.rmtree(destination)

        with zipfile.ZipFile(download_file.name, 'r') as zip:
            zip.extractall(temp_dir)

        shutil.move(os.path.join(temp_dir, "ddf--gapminder--systema_globalis-master"), destination)

    finally:
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)


def ensure_data(f):
    """Decorator that ensure the existence of data"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not CACHE_DIR.is_dir():
            logging.info(f"Cache not found, downloading data to {CACHE_DIR}")
            download_data(CACHE_DIR)
        return f(*args, **kwargs)
    
    return decorated


@ensure_data
def list_columns() -> List[str]:
    column_files = list(CACHE_DIR.glob("ddf--datapoints--*--by--geo--time.csv"))
    columns = [re.match("ddf--datapoints--(.+)--by--geo--time", f.stem)[1] for f in column_files]
    return columns   


@ensure_data
def column_details() -> pandas.DataFrame:
    return pandas.read_csv(CACHE_DIR / "ddf--concepts.csv").set_index("concept")


@ensure_data
def read_column(name: str) -> pandas.Series:
    path = CACHE_DIR / f"ddf--datapoints--{name}--by--geo--time.csv"
    return pandas.read_csv(path).set_index(["geo", "time"]).iloc[:,0]


@ensure_data
def read_columns(names: Iterable[str]) -> pandas.DataFrame:
    data_frames = [read_column(name) for name in names]
    return pandas.concat(data_frames, axis=1)


@lru_cache(1)
@ensure_data
def read_countries() -> pandas.DataFrame:
    return pandas.read_csv(CACHE_DIR / "ddf--entities--geo--country.csv").set_index("country")


def translate(df: pandas.DataFrame, countries: bool=True, columns: bool=True) -> pandas.DataFrame:
    countries = read_countries()
    columns = column_details()
