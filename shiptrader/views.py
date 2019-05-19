from django.shortcuts import render
from django.http import QueryDict
# Create your views here.

import locale
import json
import requests

from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db.models import FieldDoesNotExist

from .models import Starship, Listing


def error_message(err_code, err_message, err_details):
    return JsonResponse({
        'error_message': err_message,
        'error_details': err_details
    }, status=err_code)


def load_ships():
    url = "http://swapi.co/api/starships/"
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    if not Starship.objects.all().count():
        while url:
            contents = requests.get(url).json()
            url = contents['next']
            for ship in contents['results']:
                Starship(name=ship['name'],
                         starship_class=ship['starship_class'],
                         manufacturer=ship['manufacturer'],
                         length=float(ship['length'].replace(',', '') if ship['length'] != 'unknown' else 0),
                         hyperdrive_rating=float(ship['hyperdrive_rating'] if ship['hyperdrive_rating'] != 'unknown' else 0),
                         cargo_capacity=int(ship['cargo_capacity'] if ship['cargo_capacity'] != 'unknown' else 0),
                         crew=int(ship['crew'] if ship['crew'] != 'unknown' else 0),
                         passengers=int(ship['passengers'] if ship['passengers'] != 'unknown' else 0)).save()

    return HttpResponse(status=201)


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
    return JsonResponse(results, safe=False)


def create_listing(**kwargs):
    try:
        Listing.objects.get(name=kwargs.get('name'))
        return error_message(422, 'Not unique', f'Listing with name {kwargs.get("name")} exists!')
    except ObjectDoesNotExist:
        new_added = Listing(name=kwargs.get('name'), ship_type=Starship.objects.get(name=kwargs.get('name')), price=kwargs.get('price'), active=True)
        new_added.save()
    return JsonResponse({'id': new_added.id}, status=201)


def set_listing(list_id, **kwargs):
    active = None
    if kwargs.get("op") == "activate":
        active = True
    if kwargs.get("op") == "deactivate":
        active = False
    if active is not None:
        entry = Listing.objects.get(id=list_id)
        entry.active = active
        entry.save()
    else:
        return error_message(400, 'Invalid request', f'Unsupported operation: {kwargs.get("op")}')

    return HttpResponse(status=204)


def ships(request):
    if request.method == 'GET':
        return get_all_ships()
    elif request.method == 'POST':
        return load_ships()
    else:
        return error_message(400, 'Invalid request', f'Unsupported request: {request.method}')


def listings(request):
    if request.method == 'GET':
        return get_listings(request.GET.get('starship_class'), request.GET.get('sort', ''))
    elif request.method == 'POST':
        return create_listing(**json.loads(request.body))
    else:
        return error_message(400, 'Invalid request', f'Unsupported request: {request.method}')


def listing_detail(request, list_id):
    if request.method == 'PATCH':
        return set_listing(list_id, **json.loads(request.body))
    else:
        return error_message(400, 'Invalid request', f'Unsupported request: {request.method}')
