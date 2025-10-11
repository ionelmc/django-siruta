import json

from django import forms
from django.views import generic

from siruta.forms import CountyField
from siruta.forms import LocalityField


class DemoForm(forms.Form):
    county = CountyField(label="Delivery county")
    locality = LocalityField(label="Delivery locality")

    billing_county = CountyField()
    billing_locality = LocalityField(county_field="billing_county")


class DemoView(generic.FormView):
    template_name = "demo.html"
    form_class = DemoForm
    success_url = "/thanks/"

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(data=json.dumps(form.cleaned_data, indent=4)))
