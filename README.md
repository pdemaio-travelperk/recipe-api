# recipe-api

## How to run
docker-compose build

docker-compose up

## Apis 
### Get all recipes
GET http://localhost:8000/api/recipes/

Expected output HTTP 200-OK:
```
[
    {
        "id": 3,
        "name": "paella",
        "description": "Put it in the oven",
        "ingredients": [
            {
                "name": "tomato"
            },
            {
                "name": "cheese"
            },
            {
                "name": "dough"
            }
        ]
    },
    {
        "id": 1,
        "name": "Pizza",
        "description": "Put it in the oven",
        "ingredients": [
            {
                "name": "tomato"
            },
            {
                "name": "cheese"
            },
            {
                "name": "dough"
            }
        ]
    }
]
```
### Search recipes
GET http://localhost:8000/api/recipes/?name=TOKEN

Where TOKEN is a case-sensitive substring to search

Expected output is the same as GET all recipes

### Get recipe by id
GET http://localhost:8000/api/recipes/1

Expected output HTTP 200-OK:
```
{
        "id": 1,
        "name": "paella",
        "description": "Put it in the oven",
        "ingredients": [
            {
                "name": "tomato"
            },
            {
                "name": "cheese"
            },
            {
                "name": "dough"
            }
        ]
    }
```
---
### Create recipe

POST http://localhost:8000/api/recipes/

Payload:
```
{
        "name": "paella",
        "description": "Put it in the oven",
        "ingredients": [
            {
                "name": "tomato"
            },
            {
                "name": "cheese"
            },
            {
                "name": "dough"
            }
        ]
    }
```
Expected output HTTP 201-CREATED:
```
{
        "id": 1,
        "name": "paella",
        "description": "Put it in the oven",
        "ingredients": [
            {
                "name": "tomato"
            },
            {
                "name": "cheese"
            },
            {
                "name": "dough"
            }
        ]
    }
```
---
### Update recipe
PATCH http://localhost:8000/api/recipes/1/

Payload:
```
{
        "name": "Paella",
        "description": "Put it in the oven",
        "ingredients": [
            {
                "name": "squid"
            }
        ]
    }
```
Expected output HTTP 200-OK:
```
{
        "id": 1,
        "name": "Paella",
        "description": "Put it in the oven",
        "ingredients": [
            {
                "name": "squid"
            }
        ]
    }
```
---
### Delete recipe
DELETE http://localhost:8000/api/recipes/1/

Expected output HTTP 204-NO CONTENT
