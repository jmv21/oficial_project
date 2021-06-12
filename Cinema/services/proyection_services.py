from datetime import datetime

from Cinema.models.Actor import Actor, Discount

from Cinema.models.Hall import Hall, Seat
from Cinema.models.Actor import Actor

from Cinema.models.Movie import Movie
from Cinema.models.Projection import Projection
from Cinema.models.Hall import Seat
# from Cinema.models.Discount import Discount
from django.db.models import Sum
from django.db.models import F


def actors_query():
    return Actor.objects.all()


def movies_query():
    return Movie.objects.all()


def projection_query():
    return Projection.objects.filter(active=True)


def all_projections_query():
    return Projection.objects.all()


def update_projections_query():
    proj = projection_query().values('id', 'time__ending_time')
    ids = list(proj.values_list('id', flat=True))
    times = list(proj.values_list('time__ending_time', flat=True))

    cdate = datetime.now()
    ids_to_update = []

    # Store all expired projections
    for i in range(0, len(times)):

        if cdate >= times[i]:
            ids_to_update.append(ids[i])

    Projection.objects.filter(id__in=ids_to_update).update(active=False)


def all_discounts_query():
    return Discount.objects.all()


def active_discounts_query():
    # Get all active discounts
    all_actives = Discount.objects.all().values('type', 'amount').filter(active=True)
    # Make a list of both types and amounts
    types = list(all_actives.values_list('type'))
    amounts = list(all_actives.values_list('amount'))

    result_list = []
    kt = 0
    # Get the first and larger group of discounts which total amounts is less than 100
    for i in range(0, len(amounts)):

        kt += amounts[i]
        if kt > 100:
            break

        result_list.append(types[i])

    return Discount.objects.all().filter(type__in=result_list)


def discount_update_active(options, all_inactive=False):
    if not all_inactive:
        Discount.objects.filter(id__in=options).update(active=True)
        Discount.objects.exclude(id__in=options).update(active=False)
    else:
        Discount.objects.update(active=False)
        a = Discount.objects.all().values_list()
        print(a)

def get_spec_proj(id):
    return Projection.objects.get(id=id)

def seats_query(id):
    return Seat.objects.filter(hall_id=id)
