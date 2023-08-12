# AIQ powerplants-API

### Build using Django, DRF

## Documentation:
### API request:
   /api/powerplants/

### API Response:
  Sorted in descending order of annual net Generation 
```sh
  {
    "count": 11393,
    "next": "{Your_api_backend_server_link(example:localhost:8000/)}/api/powerplants/?limit=10&offset=10",
    "previous": null,
    "results": [
        {
            "id": 382,
            "plant_name": "Palo Verde",
            "plant_state": "AZ",
            "annual_net_generation": 31629862,
            "longitude": -112.8617,
            "latitude": 33.3881,
            "percentage": 29.15
        },
        ...
    ]
}
```
Here:
  "count" is the number of powerplants
  "next": Next API url link for paginated data
  "previous": Url link for previously paginated data
  "results": results arrays for powerplants objects as api response

  for powerplants' object, we have:
  "id":unique primary key
  "plant_name"
  "plant_state"
  "annual_net_generation": Net annual generation in MWh
  "longitude" and "latitude" : geometry coordinates of the plant
  "percentage": Percentage of the annual net generation of the plant to its federal state

## Methods allowed: 
"GET", "POST":

* "GET":
  ``` sh
  /api/powerplants/
  ```
  : following api endpoint allows both authenticated and non-authenticated users to fetch the data , for authentication users can use "Authorization Header": Bearer {token} generated from sending a POST request to: 
  ``` sh
  /api/token/
  ```
  and pass username and password in body to authorise yourself, currently you  can pass username="Mukul" and password="Django@1234"(Not   a superuser)
  which will provide :

  ``` sh
  {
    "refresh": "eyJhb...",
    "access": "eyJh..."
  }
  ```
  and you can now successfully fetch data as authorised user using "access" token, on expiring use
  ``` sh
  /api/token/refresh/
  ```
  by passing refersh token in authorization header

* "POST":
  ``` sh
  /api/powerplants/
  ```
  Only a superuser can add a new powerplant

  

## Pagination :
By default response.data.results is an array which(by default) contains 10 powerplants data as paginated , but the user can customize it to display top 'N' Plants by passing n={user_specified_number} in the query params as:
[http://localhost:8000/api/powerplants/?n=5](http://localhost:8000/api/powerplants/?n=5)

## Authentication:
Following api uses JWTAuthentication

## Filters:
Here, following are the various filters one can use:

* "STATE" Filter:
  [http://localhost:8000/api/powerplants/?state=AK](http://localhost:8000/api/powerplants/?state=AK)
  
  Fetches all the powerplants present in the given state.

* Min_net_generation filter:
  [http://localhost:8000/api/powerplants/?min_net_generation=3140000](http://localhost:8000/api/powerplants/?min_net_generation=3140000)

  Fetches only those powerplants whose minimum net annual generation is {min_annual_generation}

* Max_net_generation filter:
  [http://localhost:8000/api/powerplants/?max_net_generation=3140000](http://localhost:8000/api/powerplants/?max_net_generation=3140000)
  Fetches only those powerplants whose maximum net annual generation is {max_annual_generation}

## Caching:
Caching is done to prevent unnecessay re-querying database:
All "GET" data requests are cached to 5 minutes.

## API Rate Throttling:

``` sh
For anonymous users: 100/minute
For authenticated users: 200/minute
```


