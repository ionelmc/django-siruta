from django import forms

from siruta.forms import CountyField
from siruta.forms import LocalityField


class Form(forms.Form):
    locality = LocalityField()
    county = CountyField()


def test_form_valid():
    form = Form({"locality": "1026", "county": "1"})
    assert form.is_valid(), form.errors
    assert form.cleaned_data == {
        "county": 1,
        "locality": 1026,
    }


def test_form_bad_locality():
    form = Form({"locality": "1", "county": "1"})
    assert not form.is_valid()
    assert form.errors == {
        "locality": ["Invalid locality ID '1'."],
    }


def test_form_bad_locality_county():
    form = Form({"locality": "1", "county": "2"})
    assert not form.is_valid()
    assert form.errors == {
        "locality": ["Invalid locality ID '1'."],
    }


def test_form_bad_county():
    form = Form({"locality": "1", "county": "9999"})
    assert not form.is_valid()
    assert form.errors == {
        "county": ["Select a valid choice. 9999 is not one of the available choices."],
        "locality": ["Invalid county ID '9999'."],
    }
