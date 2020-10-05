from django.apps import AppConfig


class ContactsAppConfig(AppConfig):
    name = "contacts"
    verbose_name = "Contacts"

    def ready(self):
        try:
            import contacts.signals
        except ImportError:
            pass
