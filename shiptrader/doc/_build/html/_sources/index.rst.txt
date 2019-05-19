.. shiptrader documentation master file, created by
   sphinx-quickstart on Sun May 19 16:28:51 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================================
Welcome to shiptrader's documentation!
======================================
Shiptrader provides a group of REST API to help selling starships. It sources some technical information about the Starships on sale from the Starship API.

Starships
===================

::

    GET /shiptrader/ships/

Browse all starships.

Example esponses::

    HTTP/1.0 200 OK
    Content-Type: application/json
    [
        {
            "name": "Executor",
            "starship_classship": "Star dreadnought",
            "length": 19000,
            "hyperdrive_rating": 2,
            "cargo_capacity": 250000000,
            "crew": 279144,
            "passengers": 38000
        },
        {
            "name": "Sentinel-class landing craft",
            "starship_classship": "landing craft",
            "length": 38,
            "hyperdrive_rating": 1,
            "cargo_capacity": 180000,
            "crew": 5,
            "passengers": 75
        }
    ]

.. table::
    :widths: 30, 6, 64
    :align: left

    =================  ======  =======
    Attribute          Type    Remarks
    =================  ======  =======
    name               string  The name of this starship. The common name, such as "Death Star".
    starship_class     string  The class of this starship, such as "Starfighter" or "Deep Space Mobile Battlestation"
    length             number  The length of this starship in meters.
    hyperdrive_rating  number  The class of this starships hyperdrive.
    cargo_capacity     number  The maximum number of kilograms that this starship can transport.
    crew               number  The number of personnel needed to run or pilot this starship.
    passengers         number  The number of non-essential people this starship can transport.
    =================  ======  =======

Listings
========

::

    POST /shiptrader/listings/

List a starship for sale, the user should supply the Starship name and list price.

Example request::

    Content-Type: application/json
    {
        "name": "Belbullab-22 starfighter",
        "price": 61
    }

=================  ======  =======
Attribute          Type    Remarks
=================  ======  =======
name               string  The name of this starship. The common name, such as "Death Star".
price              number  The price of this startship for sale.
=================  ======  =======

Example responses::

    HTTP/1.0 201 Created
    Content-Type: application/json
    {
        "id": 1
    }

=================  ======  =======
Attribute          Type    Remarks
=================  ======  =======
id                 number  The name of this starship. The common name, such as "Death Star".
=================  ======  =======


::

    GET /shiptrader/listings/

Return all active listings via starship_class. Results can be sorted by price or time of listing.

Example request::

    /shiptrader/listings/?starship_class=starfighter&sort=time_submitted

=================  ======  =======
Query parameter    Type    Remarks
=================  ======  =======
starship_class     string  The class of this starship, such as "Starfighter" or "Deep Space Mobile Battlestation".
sort               string  Either "time_submitted" or "price"
=================  ======  =======


Example responses::

    HTTP/1.0 200 OK
    Content-Type: application/json
    [
        {
            "id": 1,
            "name": "Belbullab-22 starfighter",
            "price": 61,
            "time_submitted": "2019-05-19T15:06:34.697Z"
        },
        {
            "id": 2,
            "name": "arc-170",
            "price": 25,
            "time_submitted": "2019-05-19T16:32:45.451Z"
        }
    ]

=================  ========  =======
Attribute          Type      Remarks
=================  ========  =======
id                 number    The name of this starship. The common name, such as "Death Star".
name               string    The name of this starship. The common name, such as "Death Star".
price              number    The price of this startship for sale.
time_submitted     datetime  The time the listing was created.
=================  ========  =======


::

    PATCH /shiptrader/listings/id/

Update existing listing. The operation at the moment suported is: activate and deactivate. When a list is submited, it is active by default. This API can deactivate it, thus it would be hidden when browsing all listings. The activate operation can make it appear in all listings again.

Example request::

    Content-Type: application/json
    {
        "op": "activate"
    }

==========  ======  =======
Attribute   Type    Remarks
==========  ======  =======
op          string  Either "deactivate" or "deactivate"
==========  ======  =======


Example responses::

    HTTP/1.0 204 No content


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
