from itertools import chain
from typing import Iterable, Union

from django.db import models
from django.db.models import Q
from django.urls import reverse


class OrganisationManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(name__icontains=query)
                | Q(icao_code__icontains=query)
                | Q(iata_code__icontains=query)
            )
            qs = qs.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return qs


class PersonManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            qs = qs.filter(name__icontains=query).all()
        return qs


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified' fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Mode(TimeStampedModel):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class Role(TimeStampedModel):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Type(TimeStampedModel):
    name = models.CharField(max_length=35, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class KeyContact(TimeStampedModel):
    name = models.CharField(max_length=100, blank=False)
    notes = models.TextField(max_length=250, blank=True, null=True)
    tel = models.CharField(max_length=30, null=True, blank=True)
    fax = models.CharField(max_length=30, null=True, blank=True)
    surefax = models.CharField(max_length=30, null=True, blank=True)
    mobile = models.CharField(max_length=30, null=True, blank=True)
    tfh = models.BooleanField(default=False, verbose_name="24hr")
    home = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    priority = models.IntegerField(
        default=10
    )  # for sorting on detail page - low is high priority
    organisation = models.ForeignKey(
        "Organisation", null=True, blank=True, on_delete=models.CASCADE
    )

    @property
    def klass(self):
        return str(self.__class__)

    @property
    def tfh_template(self):
        """
        Pretty self.tfh for template (i.e. not True, False).
        """
        if self.tfh:
            return "YES"
        elif self.tfh is False:
            return "NO"

    def __str__(self):
        return f"{self.name}"


class Organisation(TimeStampedModel):
    name = models.CharField(max_length=100, blank=False)
    mode = models.ForeignKey(Mode, on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    main_phone = models.CharField(max_length=30, null=True, blank=True)
    iata_code = models.CharField(
        max_length=3, null=True, blank=True, verbose_name="IATA code"
    )
    icao_code = models.CharField(
        max_length=4, null=True, blank=True, verbose_name="ICAO code"
    )
    local_police = models.ForeignKey(
        "Organisation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="police_for",
    )

    objects = OrganisationManager()

    @property
    def all_persons(self):
        people = self.people.all()
        key_contacts = self.keycontact_set.all()
        return list(chain(people, key_contacts))

    @property
    def directed_person(self):
        return return_person_with_role_in_organisation(
            role_name="Directed Person", organisation=self
        )

    @property
    def people_no_directed_party(self):
        qs = self.people.exclude(role__name="Directed Person")
        return qs

    def get_absolute_url(self):
        return reverse("contacts:airport_detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class Person(TimeStampedModel):
    name = models.CharField(max_length=100, blank=False)
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name="people"
    )
    role = models.ManyToManyField(Role)
    tel = models.CharField(max_length=30, null=True, blank=True)
    fax = models.CharField(max_length=30, null=True, blank=True)
    surefax = models.CharField(max_length=30, null=True, blank=True)
    mobile = models.CharField(max_length=30, null=True, blank=True)
    home = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def klass(self):
        return str(__class__)

    objects = PersonManager()


class RemoteAmendment(TimeStampedModel):
    person_to_amend = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    key_contact_to_amend = models.ForeignKey(KeyContact, on_delete=models.CASCADE, null=True, blank=True)
    new_tel = models.CharField(max_length=30, null=True, blank=True)
    new_fax = models.CharField(max_length=30, null=True, blank=True)
    new_surefax = models.CharField(max_length=30, null=True, blank=True)
    new_mobile = models.CharField(max_length=30, null=True, blank=True)
    new_home = models.CharField(max_length=30, null=True, blank=True)
    new_priority = models.IntegerField(default=10, null=True, blank=True)
    new_role = models.CharField(max_length=100, null=True, blank=True)
    new_notes = models.TextField(max_length=250, null=True, blank=True)

# --- SELECTORS --- #

def return_person_with_role_in_organisation(
    *, role_name: str, organisation: Organisation
) -> Union[Person, None]:
    dp_role = Role.objects.get(name=role_name)
    directed_persons = Person.objects.filter(role=dp_role)
    for p in directed_persons:
        if p.organisation == organisation:
            return p
    return None

# --- END OF SELECTORS --- #
