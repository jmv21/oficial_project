from Cinema.models.Entry import Entry

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from Cinema.models.Hall import Seat

from Cinema.models.Purchase import Purchase

from Cinema.services.proyection_services import seats_query, get_spec_proj, discount_update_active, all_discounts_query


class home(TemplateView):
    template_name = 'Main_Templates/base.html'
    success_url = reverse_lazy('home')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discounts'] = all_discounts_query()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        try:
            options = request.POST.getlist('option[]')
        except:
            discount_update_active(None, True)
            return HttpResponseRedirect(self.success_url)

        discount_update_active(options)

        return HttpResponseRedirect(self.success_url)


def test(request):
    # <--Load the template--->
    template = loader.get_template('test.html')
    return HttpResponse(template.render({}, request))


class Reserves(TemplateView):
    template_name = 'reserve.html'
    success_url = reverse_lazy('home')

    def __init__(self, **kwargs):
        self.projection = None
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        proj_id = self.kwargs['hall']
        self.projection = proj_id
        proj = get_spec_proj(proj_id)
        context = self.get_context_data(**kwargs)
        context['projection'] = proj
        context['seats'] = seats_query(proj.hall_id)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        try:
            options = request.POST.getlist('option[]')
        except:
            return HttpResponseRedirect(reverse_lazy('home'))

        # Create an entry for every selected seat
        entries_list = []
        for seat in options:
            aux = Entry.create(self.projection, seat)
            entries_list.append(aux)
            aux.save(*args, **kwargs)

        email = request.POST['email']

        # NEEDED FOR THE NEXT STEP
        purchase = Purchase.create(email=email, entries=entries_list)
        Purchase.save(*args, **kwargs)

        return HttpResponseRedirect(self.success_url)
