This project is for implementation to https://github.com/ostmodern/python-code-test

It provide API documented in [here](./shiptrader/doc/_build/html/index.html)

To start:
```shell
docker-compose up
```
and ship a POST requst to

    http://localhost:8008/shiptrader/ships/
It will load all starships information from [Starship API](https://swapi.co/documentation#starships) to local database, so you can browse and create listing against.

Have fun with all the APIs!
