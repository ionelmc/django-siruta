import json

from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.choices import normalize_choices
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from .data import COUNTIES_BY_ID
from .extras import LOCALITIES_BY_COUNTY_ID
from .extras import LOCALITIES_BY_ID

COUNTY_CHOICES = (("", ""), *COUNTIES_BY_ID.items())
LOCALITY_JSON = json.dumps(
    {
        county_id: [{"text": locality_name, "value": locality_id} for locality_id, locality_name in localities.items()]
        for county_id, localities in LOCALITIES_BY_COUNTY_ID.items()
    }
)


class SelectizeSelectWidget(widgets.Select):
    template_name = "siruta/selectize_select.html"


class CountyField(forms.TypedChoiceField):
    def __init__(self, **kwargs):
        super().__init__(choices=COUNTY_CHOICES, coerce=int, **kwargs)


class LocalityWidget(widgets.TextInput):
    template_name = "siruta/locality.html"

    def __init__(self, *, county_field):
        super().__init__()
        self.county_field = county_field

    def get_context(self, name, value, attrs):
        attrs = {
            **attrs,
            "disabled": "disabled",
        }
        return {
            "county_field": self.county_field,
            "localities": mark_safe(LOCALITY_JSON),
            **super().get_context(name, value, attrs),
        }

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return value, data.get(self.county_field)

    def format_value(self, value):
        if isinstance(value, tuple):
            value, _ = value
        return super().format_value(value)


class LocalityField(forms.Field):
    def __init__(self, *, county_field="county", **kwargs):
        super().__init__(
            widget=LocalityWidget(county_field=county_field),
            **kwargs,
        )
        self.choices = normalize_choices(LOCALITIES_BY_ID)

    def to_python(self, value):
        locality_id, county_id = value

        if locality_id:
            try:
                locality_id = int(locality_id)
                county_id = int(county_id)
            except ValueError as exc:
                raise ValidationError(_("Invalid value {value}.").format(value=repr(value))) from exc

            county = COUNTIES_BY_ID.get(county_id)
            if not county:
                raise ValidationError(_("Invalid county ID '{id}'.").format(id=county_id))

            locality = LOCALITIES_BY_ID.get(locality_id)
            if not locality:
                raise ValidationError(_("Invalid locality ID '{id}'.").format(id=locality_id))

            county_localities = LOCALITIES_BY_COUNTY_ID[county_id]
            if locality_id not in county_localities:
                raise ValidationError(
                    _("Locality '{locality}' is not valid for county '{county}'.").format(
                        county=county,
                        locality=locality,
                    )
                )

            return locality_id
        else:
            return None
