# AIQ powerplants-API

### Build using Django, DRF

# Documentation:

```sh
  # API request:
   /api/powerplants/

  # API Response:
  Sorted in descending order of annual net Generation 
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

  Here:
  "count" is the number of powerplants
  "next": Next API url link for paginated data
  "previous": Url link for previously paginated data
  "results": results arrays for powerplants objects as api response
```

## Pagination :
By default response.data.results is an array which(by default) contains 10 powerplants data as paginated , but the user can customize it to display top 'N' Plants by passing n={user_specified_number} in the query params as:
[http://localhost:8000/api/powerplants/?n=5](http://localhost:8000/api/powerplants/?n=5)




