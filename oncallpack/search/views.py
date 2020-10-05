from itertools import chain

from django.views.generic import ListView

from contacts.models import Organisation, Person


class SearchView(ListView):
    template_name = "search/index.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get("q")
        # if the view contains a query, we want the "Search Results" heading in the template
        if len(self.request.GET.dict().keys()) > 0:
            context["search_results"] = True
        # otherwise not
        else:
            context["search_results"] = False
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", None)

        if query is not None:
            org_results = Organisation.objects.search(query)
            person_results = Person.objects.search(query)

            queryset_chain = chain(org_results, person_results)

            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)  # since qs is a list
            return qs
        return Organisation.objects.none()  # just an empty queryset as default
