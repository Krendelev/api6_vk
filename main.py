import os
import random
from urllib.parse import urlsplit

import requests
from dotenv import load_dotenv


def get_comics_number():
    current_number = get_comics("")[0]
    return random.randint(1, current_number + 1)


def get_comics(comics_number):
    response = requests.get(f"http://xkcd.com/{comics_number}/info.0.json")
    response.raise_for_status()
    content = response.json()
    return content["num"], content["alt"], content["img"]


def get_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def save_image(image, filename):
    with open(filename, "wb") as fh:
        fh.write(image)


def get_upload_url(payload):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    payload.update({"group_id": os.environ["VK_GROUP_ID"]})
    response = requests.get(url, params=payload)
    return response.json()["response"]["upload_url"]


def upload_picture(url, filename):
    files = {"photo": open(filename, "rb")}
    response = requests.post(url, files=files)
    return response.json()


def save_picture(payload, upload_info):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    payload.update(
        {
            "group_id": os.environ["VK_GROUP_ID"],
            "server": upload_info["server"],
            "photo": upload_info["photo"],
            "hash": upload_info["hash"],
        }
    )
    response = requests.post(url, params=payload)
    return response.json()["response"][0]


def post_picture(payload, pic_info, caption):
    url = "https://api.vk.com/method/wall.post"
    payload.update(
        {
            "owner_id": f"-{os.environ['VK_GROUP_ID']}",
            "from_group": 1,
            "message": caption,
            "attachments": f"photo{pic_info['owner_id']}_{pic_info['id']}",
        }
    )
    response = requests.get(url, params=payload)
    return response.json()["response"]


if __name__ == "__main__":

    load_dotenv()

    try:
        _, caption, url = get_comics(get_comics_number())
        image = get_image(url)
    except requests.HTTPError as error:
        exit(error)

    filename = os.path.basename(urlsplit(url).path)
    save_image(image, filename)

    payload = {"access_token": os.environ["VK_ACCESS_TOKEN"], "v": 5.101}

    upload_url = get_upload_url(payload)
    upload_info = upload_picture(upload_url, filename)
    picture_info = save_picture(payload, upload_info)
    post_picture(payload, picture_info, caption)

    os.remove(filename)
