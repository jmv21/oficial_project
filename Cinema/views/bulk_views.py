from django.shortcuts import render

# Home page view
from django.views.generic import ListView, UpdateView

from Cinema.forms import DiscountForm
# from Cinema.models.Discount import Discount
from Cinema.services import proyection_services

from Cinema.models.Actor import Actor, Discount
from Cinema.models.Movie import Movie
from Cinema.models.Projection import Projection


class MoviesListView(ListView):
    model = Movie
    template_name = 'movies.html'
    paginate_by = 2

    def get_queryset(self):
        return proyection_services.movies_query()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Movie Catalog'
        return context


def actors(request):
    actors = proyection_services.actors_query()

    context = {
        'actors': actors
    }
    return render(request, 'actors.html', context)


class ActorsListView(ListView):
    model = Actor
    template_name = 'actors.html'
    paginate_by = 2

    def get_queryset(self):
        return proyection_services.actors_query()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actors'
        return context


def projections(request):
    current_projections = proyection_services.projection_query()
    context = {
        'projections': current_projections
    }
    return render(request, 'projections.html', context)


def details(request):
    return render(request, 'movies_details.html', {})


def active_discounts(request):
    current_active_discounts = proyection_services.active_discounts_query()

    context = {
        'discounts': current_active_discounts
    }
    return render(request, 'projections.html', context)
