from django import forms
from django.forms.models import inlineformset_factory
from django.urls import reverse

from .models import Organisation, Type, KeyContact

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Fieldset,
    HTML,
    Div,
    Layout,
    Hidden,
    Field,
)

# inlineform solution from https://stackoverflow.com/a/30294290

class AirportCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse("contacts:airports_list")

        p_org = Type.objects.get(id=2)
        self.fields["local_police"].queryset = (
            Organisation.objects.filter(type=p_org).order_by("name").all()
        )

    class Meta:
        model = Organisation
        fields = [
            "name",
            "type",
            "website",
            "main_phone",
            "iata_code",
            "icao_code",
            "local_police",
        ]

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.form_class = "form-group"
        helper.form_method = "post"
        helper.layout = Layout(
            Fieldset(
                "Basics",
                HTML('<div class="row">'),
                Div('name', css_class="col-7"),
                Div('website', css_class="col"),
                HTML('</div>'),
                HTML('<div class="row">'),
                Div('iata_code', css_class="col-3"),
                Div('icao_code', css_class="col-3"),
                Div('main_phone', css_class="col"),
                HTML('</div>'),
                "local_police",
            ),
            # BERWARE! hard-coding ids for Aviation and Airport here...

            Hidden("mode", 1),
            Hidden("type", 1),
        )
        return helper


class KeyContactsHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Fieldset(
                "Add/Update key contact",
                HTML('<div class="row">'),
                Div('name', css_class="col-7"),
                Div('tel', css_class="col"),
                Div('fax', css_class="col"),
                Div('surefax', css_class="col"),
                HTML('</div>'),
                HTML('<div class="row">'),
                Div('notes', css_class="col", rows="2"),
                HTML('</div>'),
                HTML('<div class="row">'),
                Div("mobile", css_class="col"),
                Div("home", css_class="col"),
                Div("email", css_class="col"),
                Div("priority", css_class="col"),
                HTML('</div>'),
                HTML('<div class="row">'),
                Div("tfh", css_class="col"),
                Div(Field('DELETE', css_class='input-small'), css_class="col"),
                HTML('</div>'),
            )
        )


AirportFormSet = inlineformset_factory(
    Organisation,
    KeyContact,
    fields=("name", "notes", "tel", "fax", "surefax", "mobile", "home", "email", "priority", "tfh"),
    extra=1,
    can_delete=True,
)
