import os
import random
import tempfile

import requests
from dotenv import load_dotenv


def get_comics_number():
    current_number = get_comics()[2]
    return random.randint(1, current_number + 1)


def get_comics(comics_number=None):
    comics_number = comics_number or ""
    response = requests.get(f"http://xkcd.com/{comics_number}/info.0.json")
    response.raise_for_status()
    content = response.json()
    return content["img"], content["alt"], content["num"]


def get_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def get_image_extension(url):
    return url.split(".")[-1]


def check_vk_response(response):
    if "error" in response:
        raise requests.HTTPError(response["error"]["error_msg"])
    return None


def get_upload_url(payload):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    payload.update({"group_id": os.environ["VK_GROUP_ID"]})
    response = requests.get(url, params=payload).json()
    check_vk_response(response)
    return response["response"]["upload_url"]


def upload_picture(url, image):
    files = {"photo": image}
    response = requests.post(url, files=files).json()
    check_vk_response(response)
    return response


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
    response = requests.post(url, params=payload).json()
    check_vk_response(response)
    return response["response"][0]


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
    response = requests.get(url, params=payload).json()
    check_vk_response(response)
    return response["response"]


if __name__ == "__main__":

    load_dotenv()

    try:
        url, caption, _ = get_comics(get_comics_number())
        image = get_image(url)
    except requests.HTTPError as error:
        exit(error)

    extension = get_image_extension(url)
    temp = tempfile.NamedTemporaryFile(suffix=f".{extension}")
    temp.write(image)
    temp.seek(0)

    payload = {"access_token": os.environ["VK_ACCESS_TOKEN"], "v": 5.101}

    try:
        upload_url = get_upload_url(payload)
        upload_info = upload_picture(upload_url, temp)
        picture_info = save_picture(payload, upload_info)
        post_picture(payload, picture_info, caption)
    except requests.HTTPError as error:
        print(error)
    finally:
        temp.close()
