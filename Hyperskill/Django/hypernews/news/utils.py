import json
from datetime import datetime
from random import randint, choice


def get_json():
    """ Load json string. """
    with open('hypernews/news.json', 'r') as jfile:
        JSON = json.load(jfile)
    return JSON


def add_post(created, text, title, link):
    """ Append json file with new post. """
    with open('hypernews/news.json', 'r+') as jfile:
        JSON = json.load(jfile)
        JSON.append({
            "created": created,
            "text": text,
            "title": title,
            "link": link,
        })
        jfile.seek(0)
        json.dump(JSON, jfile, separators=(',', ': '))


def group_by_date(pattern=None):
    """ Group post by creation date. """

    """
    Prepares date for main page view.
    If 'pattern' parameter is provided, only posts
    with matching titles are sent to view function.
    """
    json_data = get_json()
    by_date = {}
    for obj in json_data:
        if (pattern and pattern in obj['title']) or not pattern:
            dt_str = obj['created']
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            created = dt.strftime("%Y-%m-%d")
            if created not in by_date:
                by_date[created] = []
            temp_dict = {}
            for k, v in obj.items():
                if k != 'created':
                    temp_dict[k] = v
            by_date[created].append(temp_dict)
    return by_date


def get_post_data():
    """ Get timestamp and ID """

    """
    Creates randomized ID and gets current time for a new post.
    """
    dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    while (i := randint(1, 9999999)) in [obj['link'] for obj in get_json()]:
        continue
    else:
        post_id = i
    return dt_str, post_id
