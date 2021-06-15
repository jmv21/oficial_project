import json

from django.core import serializers

from Cinema.models.Projection import Entry

from django.db.models import ManyToManyField

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView


from Cinema.models.Purchase import Purchase

from Cinema.services.proyection_services import seats_query, get_spec_proj, discount_update_active, all_discounts_query, \
    all_movies_query, active_discounts_query, available_entries_query


class home(TemplateView):
    template_name = 'Main_Templates/base.html'
    success_url = reverse_lazy('home')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discounts'] = all_discounts_query()
        context['movies'] = all_movies_query()[:5]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            options = request.POST.getlist('checked[]')
        except:
            discount_update_active(None, True)
            return JsonResponse({})
        discount_update_active(options)
        data = serializers.serialize('json', all_discounts_query())
        return JsonResponse(data, safe=False)


class Reserves(TemplateView):
    template_name = 'reserve.html'
    success_url = reverse_lazy('home')

    def __init__(self, **kwargs):
        self.projection = None
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discounts'] = all_discounts_query()
        return context

    def get(self, request, *args, **kwargs):
        proj_id = self.kwargs['hall']
        self.projection = proj_id
        proj = get_spec_proj(proj_id)
        context = self.get_context_data(**kwargs)
        context['projection'] = proj
        context['entries'] = available_entries_query(proj)
        context['active_discounts'] = active_discounts_query()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            options = request.POST.getlist('reserved[]')
        except:
            return HttpResponseRedirect(reverse_lazy('home'))

        email = request.POST['email']

        purchase = Purchase.create(email=email, entries=ManyToManyField, discounts=ManyToManyField)

        for entry in options:
            purchase.entries.add(entry)

        # If discounts were chosen
        try:
            options = request.POST.getlist('active_discount[]')
        except:
            purchase.save(*args, **kwargs)
            return HttpResponseRedirect(self.success_url)

        # Add all selected discounts
        discounts_per_entry = []
        for item in options:
            discounts_per_entry.append(str(item).split(","))

        # Add to each entry the corresponding discounts
        for i in range(0, len(discounts_per_entry)):
            for item in discounts_per_entry[i]:
                purchase.entries[i].add(item)

        purchase.save(*args, **kwargs)

        return HttpResponse(self.success_url)

