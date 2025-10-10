from siruta.extras import clean_locality_name


def test_clean_locality_name():
    assert clean_locality_name(" a - bc.d . EfG . - ") == "A BC D EFG"
