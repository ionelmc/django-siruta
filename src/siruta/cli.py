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
import csv
import enum
import json
import operator
from pathlib import Path

import msgspec
from unidecode import unidecode

data_path = Path("data")
parser = argparse.ArgumentParser(description="Command description.")
parser.add_argument(
    dest="localities_file",
    metavar="CSV",
    default=data_path / "siruta_an_2024.csv",
    nargs="?",
    type=Path,
    help="Input CSV file. Default: %(default)s",
)
parser.add_argument(
    dest="counties_file",
    metavar="CSV",
    default=data_path / "siruta-judete.csv",
    nargs="?",
    type=Path,
    help="Input CSV file. Default: %(default)s",
)
parser.add_argument(
    "--dialect",
    "-d",
    default="excel",
    help=f"CSV dialect to use. Available: {csv.list_dialects()}",
)
parser.add_argument(
    "--output-path",
    "-o",
    default=Path("src", "siruta"),
    type=Path,
)


class SirutaTypes(enum.IntEnum):
    """
    https://legislatie.just.ro/public/DetaliiDocument/46083

        0	Judet, municipiul Bucuresti
        1	Municipiu
        2	Oras ce apartine de judet
        3	Comuna
        4	Oras declarat municipiu
        5	Oras ce apartine de municipiu
        6	Comuna suburbana ce apartine de municipiu
        7	Oras fara localitate subordonata, ce apartine de judet
        8	Comuna suburbana ce apartine de judet
        9	Localitate componenta a orasului de resedinta declarata municipiu
        10	Celelalte localitati sau sectoare componente ale orasului declarat municipiu
        11	Sat ce apartine de orasul declarat municipiu
        12	Localitate componenta (resedinta orasului ce apartine de municipiu)
        13	Celelalte localitati componente ce apartin orasului care este subordonat municipiului
        14	Sat apartinind unui oras subordonat municipiului
        15	Sat resedinta de comuna suburbana care apartine de municipiu
        16	Celelalte sate care apartin comunei suburbane subordonate unui municipiu
        17	Localitate componenta (resedinta orasului care apartine de judet)
        18	Celelalte localitati componente ale uni oras ce apartine de judet
        19	Sate subordonate unui oras ce apartine de judet
        20	Sat resedinta de comuna suburbana subordonata unui oras care apartine de judet
        21	Celelalte sate apartinind de o comuna suburbana subordonate unui oras apartinind judetului
        22	Sat resedinta de comuna
        23	Sat component al comunei
    """

    judet = 40  # Judet, municipiul Bucuresti
    municipiu_rdj = 1  # Municipiu resedinta de judet, municipiul Bucuresti
    oras = 2  # Oras ce apartine de judet, altele decit  resedinta de judet
    comuna = 3  # Comuna
    municipiu = 4  # Municipiu, altele decit resedinta de judet
    oras_rdj = 5  # Oras resedinta de judet
    sector = 6  # Sectoarele municipiului Bucuresti
    localitate_crm = 9  # Localitate componenta, resedinta de municipiu
    localitate_cm = 10  # Localitate componentă, a unui municipiu alta decât reşedinţă de municipiu
    sat_m = 11  # Sat ce apartine de municipiu
    localitate_cro = 17  # Localitate componenta (resedinta orasului care apartine de judet)
    localitate_co = 18  # Localitati componente ale orasului altele decit resedinta de oras
    sat_o = 19  # Sate subordonate unui oras
    sat_rc = 22  # Sat resedinta de comuna
    sat_c = 23  # Sat ce apartine de comuna, altele decit resedinta de comuna


SIRUTA_TYPE_REORDER = (
    SirutaTypes.judet,
    SirutaTypes.sector,
    SirutaTypes.municipiu_rdj,
    SirutaTypes.municipiu,
    SirutaTypes.localitate_crm,
    SirutaTypes.oras_rdj,
    SirutaTypes.oras,
    SirutaTypes.localitate_cro,
    SirutaTypes.localitate_cm,
    SirutaTypes.localitate_co,
    SirutaTypes.sat_m,
    SirutaTypes.sat_o,
    SirutaTypes.comuna,
    SirutaTypes.sat_rc,
    SirutaTypes.sat_c,
)


class SirutaLevel(enum.IntEnum):
    judet = 1  # Judeţe, Municipiul Bucureşti
    municipiu = 2  # Municipii
    localitate = 5  # Localităţi componente
    oras = 3  # Oraşe
    sat = 6  # Sate
    comuna = 4  # Comune
    sector = 7  # Sectoare ale capitalei


class SirutaArea(enum.IntEnum):
    judet = 0
    urban = 1
    rural = 3


class SirutaCountyRow(msgspec.Struct):
    id: int = msgspec.field(name="JUD")
    name: str = msgspec.field(name="DENJ")
    order: int = msgspec.field(name="FSJ")
    code: str = msgspec.field(name="MNEMONIC")
    area: int = msgspec.field(name="ZONA")


class SirutaRow(msgspec.Struct):
    id: int = msgspec.field(name="SIRUTA")
    name: str = msgspec.field(name="DENLOC")
    county: int = msgspec.field(name="JUD")
    parent: int = msgspec.field(name="SIRSUP")
    type: SirutaTypes = msgspec.field(name="TIP")
    level: SirutaLevel = msgspec.field(name="NIV")
    area: SirutaArea = msgspec.field(name="MED")
    region: int = msgspec.field(name="REGIUNE")
    county_order: int = msgspec.field(name="FSJ")
    alpha_order: str = msgspec.field(name="FSL")

    ascii_name: str = None
    children: list = msgspec.field(default_factory=list)

    def __post_init__(self):
        self.ascii_name = unidecode(self.name)


SIRUTA_ROW_ORDERING_KEY = operator.attrgetter("ordering_key")


def run(args=None):
    args = parser.parse_args(args=args)
    county_codes = {}
    with args.counties_file.open() as stream:
        reader = csv.DictReader(stream, dialect=args.dialect, delimiter=";")
        fields = reader.fieldnames
        print(f"Reading {args.counties_file!r} with fields: {fields!r}")
        for row in reader:
            row = msgspec.convert(row, type=SirutaCountyRow, strict=False)
            county_codes[row.id] = row.code

    with args.localities_file.open() as stream:
        reader = csv.DictReader(stream, dialect=args.dialect)
        fields = reader.fieldnames
        print(f"Reading {args.localities_file!r} with fields: {fields!r}")
        counties = {}
        localities_by_county = {}
        entries = {}
        rows = {}
        for row in reader:
            row = msgspec.convert(row, type=SirutaRow, strict=False)
            rows[row.id] = row

            if row.type == SirutaTypes.judet:
                counties[row.county] = row.name.removeprefix("JUDETUL ").removeprefix("JUDEŢUL ").removeprefix("MUNICIPIUL ")
                assert row.county in county_codes
                localities_by_county[row.county] = []

            entries[row.id] = row
            if row.parent > 1:
                entries[row.parent].children.append(row)

        for row in entries.values():
            if not (row.type == SirutaTypes.judet or row.children):
                localities_by_county[row.county].append(row)

        def ordering_key(row):
            if row.parent > 1:
                return SIRUTA_TYPE_REORDER.index(row.type), *ordering_key(rows[row.parent]), row.ascii_name
            else:
                return SIRUTA_TYPE_REORDER.index(row.type), row.ascii_name

        localities_by_county_by_id = {}
        for county, localities in localities_by_county.items():
            localities_by_county_by_id[county] = localities_by_id = {}
            localities.sort(key=ordering_key)
            for locality in localities:
                localities_by_id[locality.id] = locality.name

        with args.output_path.joinpath("data.py").open("w") as consts_fh:
            consts_fh.write("COUNTY_IDS_BY_CODE = {\n    ")
            consts_fh.write("\n    ".join(f'"{v}": {k!r},' for k, v in county_codes.items()))
            consts_fh.write("\n}\n")
            consts_fh.write("COUNTY_CODES_BY_ID = {code: county_id for county_id, code in COUNTY_IDS_BY_CODE.items()}\n\n")
            consts_fh.write("COUNTIES_BY_ID = {\n    ")
            consts_fh.write("\n    ".join(f'{k!r}: "{v}",' for k, v in counties.items()))
            consts_fh.write("\n}\n\nLOCALITIES_BY_COUNTY_ID = {")
            for county_id, localities in localities_by_county_by_id.items():
                consts_fh.write(f"\n    {county_id!r}: {{  # {counties[county_id]}\n        ")
                consts_fh.write("\n        ".join(f'{k!r}: "{v}",' for k, v in localities.items()))
                consts_fh.write("\n    },")
            consts_fh.write("\n}\n")

        with args.output_path.joinpath("static", "siruta", "counties.js").open("w") as fh:
            fh.write("const COUNTIES = ")
            json.dump(
                {
                    "RO": [
                        {"value": "", "text": ""},
                        *[{"value": county_codes[county_id], "text": name} for county_id, name in counties.items()],
                    ]
                },
                fh,
            )
            fh.write(";\nconst LOCALITIES = ")
            json.dump(
                {
                    county_codes[county_id]: [
                        {"value": "", "text": ""},
                        *[{"value": unidecode(name), "text": name} for name in localities.values()],
                    ]
                    for county_id, localities in localities_by_county_by_id.items()
                },
                fh,
            )
            fh.write(";\n")
