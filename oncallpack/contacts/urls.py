from django.views.generic.base import TemplateView

from django.urls import path

from contacts.views import (
    OrganisationListView,
    AirportListView,
    AirportCreateView,
    AirportDetailView,
    AirportContactsView,
    airport_update,
    PoliceListView,
)

app_name = "contacts"
urlpatterns = [
    path("", TemplateView.as_view(template_name="contacts/contacts_index.html")),
    path("organisations/", OrganisationListView.as_view(), name="organisations_list"),
    path("airports/", AirportListView.as_view(), name="airports_list"),
    path("police/", PoliceListView.as_view(), name="police_list"),
    path("create-airport/", AirportCreateView.as_view(), name="airport_create"),
    path("update-airport/<int:org_id>", airport_update, name="airport_update"),
    path("airport/<int:pk>", AirportDetailView.as_view(), name="airport_detail"),
    path("airport-contacts/<int:pk>", AirportContactsView.as_view(), name="airport_detail_contacts")
]
