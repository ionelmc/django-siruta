"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -msiruta` python will execute
    ``__main__.py`` as a script. That means there will not be any
    ``siruta.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there"s no ``siruta.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import niquests

from .data import COUNTIES_BY_ID
from .data import LOCALITIES_BY_COUNTY_ID
from .data import LOCALITY_ALIASES

logger = logging.getLogger(__name__)
data_path = Path("data")
parser = argparse.ArgumentParser(description="Command description.")
parser.add_argument(
    dest="county_endpoint",
    metavar="URL",
    help="Localities data endpoint. Example: https://webnom.anaf.ro/Nomenclatoare/api/judete",
)
parser.add_argument(
    "--force-refresh",
    "-f",
    dest="cache",
    action="store_false",
    help="Skips caches.",
)
parser.add_argument(
    "--output-path",
    "-o",
    default=Path("src", "siruta"),
    type=Path,
)
parser.add_argument(
    "--log-level",
    "-l",
    default=logging.getLevelName("INFO"),
    type=logging.getLevelName,
)


def run(argv=None):
    args = parser.parse_args(args=argv)
    logging.basicConfig(level=args.log_level)
    endpoint = args.county_endpoint.rstrip("/")
    dest_path = data_path / "anaf"
    dest_path.mkdir(exist_ok=True)
    localities_by_county_id = {}
    for county_id, localities_by_siruta_id in LOCALITIES_BY_COUNTY_ID.items():
        localities = localities_by_county_id[county_id] = {}
        county_path = dest_path / f"{county_id}.json"
        if county_path.exists() and args.cache:
            logger.info("Reading %r", county_path)
            data = json.loads(county_path.read_text())
        else:
            url = f"{endpoint}/{county_id}"
            logger.info("Fetching %r", url)
            resp = niquests.get(url)
            data = resp.json()
            logger.info("Saving %r", county_path)
            county_path.write_text(json.dumps(data, indent=2))
        for entry in data:
            siruta_id, name = int(entry["siruta"]), entry["denumire"]
            while siruta_id in LOCALITY_ALIASES:
                siruta_id = LOCALITY_ALIASES[siruta_id]
            localities[entry["cod"]] = siruta_id, name
            if siruta_id not in localities_by_siruta_id:
                logger.warning("Unexpected siruta code for %r", entry)

    with args.output_path.joinpath("anaf.py").open("w") as consts_fh:
        consts_fh.write("LOCALITIES_TO_SIRUTA_ID = {  # ANAF ids to siruta ids")
        for county_id, localities in localities_by_county_id.items():
            localities_by_siruta_id = LOCALITIES_BY_COUNTY_ID[county_id]
            consts_fh.write(f"\n    {county_id!r}: {{  # {COUNTIES_BY_ID[county_id]}\n        ")
            consts_fh.write(
                "\n        ".join(
                    f"{k}: {siruta_id},  # {name} -> {localities_by_siruta_id[siruta_id]}"
                    if siruta_id in localities_by_siruta_id
                    else f"# {k}: {siruta_id},  # {name!r} is unknown"
                    for k, (siruta_id, name) in localities.items()
                )
            )
            consts_fh.write("\n    },")
        consts_fh.write("\n}\n")
