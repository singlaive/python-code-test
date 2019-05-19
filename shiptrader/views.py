from django.shortcuts import render
from django.http import QueryDict
# Create your views here.

import locale
import json
import requests

from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Starship, Listing

ship_store = []


def error_message(error_code, error_message, error_details):
    return JsonResponse({
        'error_code': error_code,
        'error_message': error_message,
        'error_details': error_details
    })


def load_ships():
    url = "http://swapi.co/api/starships/"
    if not ship_store:
        while url:
            contents = requests.get(url).json()
            url = contents['next']
            ship_store.extend(contents['results'])

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        for ship in ship_store:
            Starship(name=ship['name'],
                     starship_class=ship['starship_class'],
                     manufacturer=ship['manufacturer'],
                     length=float(ship['length'].replace(',', '') if ship['length'] != 'unknown' else 0),
                     hyperdrive_rating=float(ship['hyperdrive_rating'] if ship['hyperdrive_rating'] != 'unknown' else 0),
                     cargo_capacity=int(ship['cargo_capacity'] if ship['cargo_capacity'] != 'unknown' else 0),
                     crew=int(ship['crew'] if ship['crew'] != 'unknown' else 0),
                     passengers=int(ship['passengers'] if ship['passengers'] != 'unknown' else 0)).save()

    print(f'len(ship_store)={len(ship_store)}')
    # ship = Starship.objects.get(manufacturer='Corellian Engineering Corporation')
    print(list(Starship.objects.all())[0].__dict__)
    print(Starship._meta.get_fields())
    return JsonResponse({'results': ship_store})


def get_all_ships():
    all_ships = [{
        'name': entry.name,
        'starship_classship': entry.starship_class,
        'length': entry.length,
        'hyperdrive_rating': entry.hyperdrive_rating,
        'cargo_capacity': entry.cargo_capacity,
        'crew': entry.crew,
        'passengers': entry.passengers} for entry in Starship.objects.all()
    ]
    return JsonResponse(all_ships, safe=False)


def get_listings(starship_class, sort):
    for entry in Starship.objects.filter(starship_class=starship_class):
        print(f'class<{starship_class}> {entry.name}')

    for entry in Listing.objects.all():
        print(f'Listing: {entry.name} -> {entry.ship_type} {entry.active} @{entry.time_submitted}')

    if sort:
        query = Listing.objects.filter(ship_type__starship_class=starship_class).order_by(sort)
    else:
        query = Listing.objects.filter(ship_type__starship_class=starship_class)

    results = [{
            'id': entry.id,
            'name': entry.name,
            'price': entry.price,
            'time_submitted': entry.time_submitted
        } for entry in query if entry.active
    ]
    print(results)
    return JsonResponse(results, safe=False)


def create_listing(**kwargs):
    try:
        Listing.objects.get(name=kwargs.get('name'))
    except ObjectDoesNotExist:
        Listing(name=kwargs.get('name'), ship_type=Starship.objects.get(name=kwargs.get('name')), price=kwargs.get('price'), active=True).save()
    return JsonResponse({'created': True})


def set_listing(list_id, **kwargs):
    if 'op' in kwargs:
        print(f'activate = {kwargs["op"]}')
        active = None
        if kwargs["op"] == "activate":
            active = True
        if kwargs["op"] == "deactivate":
            active = False
        if active is not None:
            entry = Listing.objects.get(id=list_id)
            entry.active = active
            entry.save()

    return JsonResponse({'list_id': list_id})


def ships(request):
    if request.method == 'GET':
        return get_all_ships()
    elif request.method == 'POST':
        return load_ships()
    else:
        return error_message(500, 'damn', 'what the hell??')


def listings(request):
    if request.method == 'GET':
        return get_listings(request.GET.get('starship_class'), request.GET.get('sort', ''))
    elif request.method == 'POST':
        return create_listing(**json.loads(request.body))
    else:
        return error_message(500, 'damn', 'what the hell??')


def listing_detail(request, list_id):
    if request.method == 'PATCH':
        return set_listing(list_id, **json.loads(request.body))
    else:
        return error_message(500, 'damn', 'what the hell??')
