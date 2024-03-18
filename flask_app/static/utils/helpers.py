import requests
from apikey import apikey


def api_call(title):
    movie = f"http://www.omdbapi.com/?t={title}&apikey={apikey}"

    response = requests.get(movie)
    data = response.json()
    # print(data)
    give_back = {
        'title': data['Title'],
        'year': data['Year'],
        'genre': data['Genre'],
        'plot': data['Plot'],
        'actors': data['Actors'],
        'ratings': data['Ratings'][0]['Value'],
        'poster': data['Poster']
    }

    return give_back
