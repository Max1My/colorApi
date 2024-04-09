import requests


def get_color_name(color: str) -> str | None:
    response = requests.get(f'https://www.thecolorapi.com/id?hex={color}')
    if response.status_code == 200:
        return response.json()['name']["value"]
