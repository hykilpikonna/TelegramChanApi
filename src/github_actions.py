#!/usr/bin/python3
"""
This script will be called by GitHub Actions to update the posts json on GitHub Pages
"""

import json
import os
import sys
from pathlib import Path

import requests

from main import get_all_posts


def get_image(url: str, name: str) -> str:
    """
    Get image and return localized url

    :param url: Remote url
    :param name: File name
    :return: Localized url
    """
    # Add file extension
    extension = url.split('.')[-1]
    if len(extension) > 5:
        extension = 'jpg'
    name += '.' + extension

    # Get file path
    assets = path.joinpath('assets')
    assets.mkdir(exist_ok=True, parents=True)
    file = assets.joinpath(name)

    if os.path.isfile(file):
        print(f'Already exists: {name}')
    else:
        print(f'Downloading image {name}...')

        # Download image
        img_data = requests.get(url).content
        with open(assets.joinpath(name), 'wb') as f:
            f.write(img_data)

    return '/assets/' + name


if __name__ == '__main__':
    channel = 'hykilp'
    posts = get_all_posts(channel)

    args = sys.argv[1:]
    print(f'Args: {args}')

    # Create path
    path = Path(os.path.abspath(__file__)).parent.joinpath(args[0] if len(args) > 0 else '../docs')
    path.mkdir(exist_ok=True)

    # Download images
    for p in posts:
        for k in ['reply', 'video']:
            if k in p:
                if 'thumb' in p[k]:
                    p[k]['thumb'] = get_image(p[k]['thumb'], p['id'].zfill(4) + f'-{k}-thumb')

        if 'images' in p:
            for img in p['images']:
                image_id = img['href'].split('/')[-1].split('?')[0]
                img['url'] = get_image(img['url'], image_id.zfill(4))

    # Write file
    with open(path.joinpath('posts.json'), 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=1, ensure_ascii=False)
