#!/usr/bin/python3
"""
This script will be called by GitHub Actions to update the posts json on GitHub Pages
"""

import json
import os
from pathlib import Path

from main import get_all_posts


if __name__ == '__main__':
    channel = 'hykilp'
    posts = get_all_posts(channel)

    # Write file
    path = Path(os.path.abspath(__file__)).parent.joinpath('../generated')
    path.mkdir(exist_ok=True)
    with open(path.joinpath('posts.json'), 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=1, ensure_ascii=False)
