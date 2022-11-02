from bs4 import BeautifulSoup
import requests
import typing as tp


def get_glink(movie: str, is_film: bool) -> tp.Optional[str]:
    if is_film:
        search = f"{movie} смотреть онлайн ivi"
    else:
        search = f"{movie} смотреть онлайн сериал"

    url = 'https://www.google.com/search'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,rus,en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.82',
    }
    parameters = {'q': search}

    content = requests.get(url, headers=headers, params=parameters).text
    soup = BeautifulSoup(content, 'html.parser')

    search = soup.find(id='search')
    if search is None:
        return None

    first_link = search.find('a')
    if first_link is None:
        return None

    # print(first_link)
    return first_link['href']
