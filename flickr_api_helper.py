import requests
import os


def flickr_request(query):
    url = 'https://api.flickr.com/services/rest/'
    params = {'api_key': '', 'text': query, \
              'privacy_filter': 1, 'license': 3, 'content_type': 1, 'format': 'json', 'per_page': 1,
              "method": "flickr.photos.search", 'nojsoncallback': 1}
    request = requests.get(url, params=params)
    return request.json()


def check_for_image(query):
    query = query.strip().lower()
    word = query.replace(' ', '_') + '.jpg'
    file_list = os.listdir('./img')
    if word in file_list:
        print('Image found in database')
        path = os.path.join('/img', word)
        return path
    else:
        result = build_url(flickr_request(query), word)
        return result


def build_url(params, word):
    try:
        server_id = params['photos']['photo'][0]['server']
        id = params['photos']['photo'][0]['id']
        secret = params['photos']['photo'][0]['secret']
    except IndexError:
        return "/img/nothing_to_display.jpg"
    else:
        url = f'https://live.staticflickr.com/{server_id}/{id}_{secret}.jpg'
        print('Adding image to database')
        write_image(url, word)
        return url


def write_image(url, query):
    request = requests.get(url)
    filename = os.path.join('./img', query)
    with open(filename, 'wb') as file:
        file.write(request.content)
