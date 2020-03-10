# Test app

Uses Flask framework

Start development environment

`docker-compose up`

Tear down everything including db data

`docker-compose down --volume`

## Generate data

Will show generator help

`docker-compose exec python python gen.py`

Generates 20 random products

`python gen.py -p`

Generates 50 orders

`python gen.py -o 50`
