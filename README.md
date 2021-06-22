# cloudblue

Web Application that allows operating with Orders by making http calls to the application's API. Orders app has 3 entities:
1. Order - entity that describes what users want to buy. It has fields:
  - id
  - created_at
  - external_id
  - status

2. Product - entity that could be included in orders. It has next fields:
  - id
  - name
  
3. OrderDetail - links Product and Order entities with price and amount information. It has next fields:
  - id
  - price
  - product
  - order

# Requirements

Django 3.2, DjangoRestFramework 3.12.4.

API accepts and returns only JSON format data.
Root url for API requests: `/api/v1/`

# Usage

## GET

Get all orders:
`/api/v1/orders/`

```json
[{
    "id": 1,
    "status": "new",
    "created_at": "2021-15-06 16:27:27",
    "external_id": "gh-158-7771",
    "details": [{
        "id": 1,
        "product": {"id": 2, "name": "Sofa"},
        "amount": 10,
        "price": "12.00"
    }]
},
{
    "id": 2,
    "status": "new",
    "created_at": "2021-15-06 16:29:05",
    "external_id": "VR-888-hu-01",
    "details": [{
        "id": 2,
        "product": {"id": 1, "name": "Computer"},
        "amount": 2,
        "price": "602.00"
    }]
}
]
```

Exact order could be returned by id. For example:

`/api/v1/orders/1/`

```json
[{
    "id": 1,
    "status": "new",
    "created_at": "2021-15-06 16:27:27",
    "external_id": "gh-158-7771",
    "details": [{
        "id": 1,
        "product": {"id": 2, "name": "Sofa"},
        "amount": 10,
        "price": "12.00"
    }]
}]
```

User can filter orders via fields 'external_id' and 'status'.

## POST

Status of orders could be changed from new to 'accepted' or 'failed' using POST method and sufficient urls:

`/api/v1/orders/{id}/accept` - switched to accepted,

`/api/v1/orders/{id}/fail` - switched to failed.

```json
[{
    "id": 1,
    "status": "accepted",
    "created_at": "2021-15-06 16:27:27",
    "external_id": "gh-158-7771",
    "details": [{
        "id": 1,
        "product": {"id": 2, "name": "Sofa"},
        "amount": 10,
        "price": "12.00"
    }]
}]
```

Order entity could be created via POST method. Order's created_at, id and status fields values set automatically. Deafult status - 'New'. Created_at - current time UTC. If any data will be set by user - it will be ignored. Details and external_id fields are required.

In details product field id required. User can not create new product.

Request url: `/api/v1/orders/`

Request body:
```json
[{
    "external_id": "45p-YT-1234",
    "details": [{
        "product": {"id": 2},
        "amount": 10,
        "price": "2.00"
    }]
}]
```

Response body:

```json
[{
    "id": 3,
    "status": "new",
    "created_at": "2021-15-06 16:27:27",
    "external_id": "45p-YT-1234",
    "details": [{
        "id": 3,
        "product": {"id": 2, "name": "Sofa"},
        "amount": 10,
        "price": "2.00"
    }]
}]
```

If any required data is missed or has incorrect format - specified answer will be returned to user.


## PUT

User can change only order external_id field. All other data will be ignored. For example:

PUT url" `/api/v1/orders/3/`

Request body:

```json
[{
    "id": 88,
    "status": "failed",
    "created_at": "2021-35-06 16:27:27",
    "external_id": "45p-YT-1234-changed",
    "details": [{
        "id": 303,
        "amount": 1000,
        "price": "77.00"
    }]
}]
```


Response body:

```json
[{
    "id": 3,
    "status": "new",
    "created_at": "2021-15-06 16:27:27",
    "external_id": "45p-YT-1234-changed",
    "details": [{
        "id": 3,
        "product": {"id": 2, "name": "Sofa"},
        "amount": 10,
        "price": "2.00"
    }]
}]
```

## DELETE

User can not delete order with status 'accepted' - app will return specified response 405 and message.
