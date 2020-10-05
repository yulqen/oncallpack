from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .forms import AirportCreateForm, AirportFormSet, KeyContactsHelper
from .models import Organisation, Type


class OrganisationListView(LoginRequiredMixin, ListView):
    model = Organisation


class AirportListView(LoginRequiredMixin, ListView):
    template_name = "contacts/airports_list.html"

    def get_queryset(self):
        self.airport_type = get_object_or_404(Type, name="Airport")
        return Organisation.objects.filter(type=self.airport_type)


@login_required
def airport_update(request, org_id):
    if org_id:
        org = Organisation.objects.get(pk=org_id)
    else:
        org = Organisation()
    org_form = AirportCreateForm(instance=org)
    #   AirportFormSet = inlineformset_factory(
    #       Organisation,
    #       KeyContact,
    #       fields=("name", "notes",  "tel", "fax", "surefax", "mobile", "home", "priority", "tfh"),
    #       extra=2,
    #       can_delete=False,
    #   )
    formset = AirportFormSet(instance=org)
    if request.method == "POST":
        org_form = AirportCreateForm(request.POST)
        if org_id:
            org_form = AirportCreateForm(request.POST, instance=org)

        formset = AirportFormSet(request.POST, request.FILES)

        if org_form.is_valid():
            created_org = org_form.save(commit=False)
            formset = AirportFormSet(request.POST, request.FILES, instance=created_org)

            if formset.is_valid():
                created_org.save()
                formset.save()
                return HttpResponseRedirect(org.get_absolute_url())
    keycontacts_helper = KeyContactsHelper()
    return render(
        request,
        "contacts/update_airport.html",
        {
            "org_id": org_id,
            "org_form": org_form,
            "formset": formset,
            "keycontacts_helper": keycontacts_helper,
        },
    )


class AirportCreateView(LoginRequiredMixin, CreateView):
    model = Organisation
    template_name = "contacts/create_airport.html"
    form_class = AirportCreateForm
    success_url = reverse_lazy("contacts:airports_list")

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        airport_form = self.get_form(form_class)
        formset = AirportFormSet()

        return self.render_to_response(
            self.get_context_data(formset=formset, airport_form=airport_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        airport_form = self.get_form(form_class)
        formset = AirportFormSet(self.request.POST)

        if airport_form.is_valid() and formset.is_valid():
            return self.form_valid(airport_form, formset)

    def form_valid(self, airport_form, formset):
        self.object = airport_form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, airport_form, formset):
        return self.render_to_response(
            self.get_context_data(airport_form=airport_form, formset=formset)
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        keycontacts_helper = KeyContactsHelper

        if self.request.POST:
            ctx["airport_form"] = AirportCreateForm(self.request.POST)
            ctx["formset"] = AirportFormSet(self.request.POST)
            ctx["keycontacts_helper"] = keycontacts_helper
        else:
            ctx["airport_form"] = AirportCreateForm()
            ctx["formset"] = AirportFormSet()
            ctx["keycontacts_helper"] = keycontacts_helper
        return ctx


class AirportDetailView(LoginRequiredMixin, DetailView):
    # TODO Remove dependency: commment next two lines out to migrate for first time
    ap = Type.objects.filter(name="Airport").first()
    queryset = Organisation.objects.filter(type=ap)
    template_name = "contacts/airport_detail.html"

class AirportContactsView(DetailView):
    ap = Type.objects.filter(name="Airport").first()
    queryset = Organisation.objects.filter(type=ap)
    template_name = "contacts/airport_detail_contacts.html"

class PoliceListView(LoginRequiredMixin, ListView):
    template_name = "contacts/police_list.html"

    def get_queryset(self):
        self.police_type = get_object_or_404(Type, name="Police Force")
        return Organisation.objects.filter(type=self.police_type)
