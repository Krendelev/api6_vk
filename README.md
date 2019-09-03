# Comics publisher

Posts random [xkcd](https://xkcd.com) comics to [VK](https://vk.com) group wall.

### How to install

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Create your [VK](https://vk.com) group and app to post images. Get your [access_token](https://vk.com/dev/implicit_flow_user) and put it along with `group_id` into the `.env` file.

```bash
VK_GROUP_ID=some_digit
VK_ACCESS_TOKEN=some_very_long_digit
```

```bash
$ python main.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
