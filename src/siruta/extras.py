import re

from unidecode import unidecode

from .data import LOCALITIES_BY_COUNTY_ID


def clean_locality_name(value, regex=re.compile(r"[-.\s]+")):
    return regex.sub(" ", unidecode(value)).strip().upper()


LOCALITIES_BY_ID = {
    locality_id: locality_name for localities in LOCALITIES_BY_COUNTY_ID.values() for locality_id, locality_name in localities.items()
}
LOCALITIES_BY_COUNTY_ID_BY_NAME = {
    county_id: {clean_locality_name(locality_name): locality_id for locality_id, locality_name in localities.items()}
    for county_id, localities in LOCALITIES_BY_COUNTY_ID.items()
}
