import re

import cssutils
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


def to_text(element) -> str:
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, str):
            text += elem.strip()
        elif elem.name == 'br':
            text += '\n'
    return text


def parse_post(msg: Tag) -> dict:
    post = {}
    # post['data-post'] = msg.attrs['data-post']
    post['id'] = msg.attrs['data-post'].split('/')[-1]
    # post['data_view'] = msg.attrs['data-view']
    if 'service_message' in msg.attrs['class']:
        post['type'] = 'service'

    reply = msg.select_one('.tgme_widget_message_reply')
    if reply is not None:
        rep = {}
        rep['url'] = reply.attrs['href']
        text = reply.select_one('.tgme_widget_message_metatext')
        if text is None:
            text = reply.select_one('.tgme_widget_message_text')
        rep['text'] = text.text
        tmp = reply.select_one('.tgme_widget_message_reply_thumb')
        if tmp is not None:
            rep['thumb'] = get_bg_image(tmp.attrs['style'])
        post['reply'] = rep

    video = msg.select_one('.tgme_widget_message_video_player')
    if video is not None:
        vid = {}
        thumb = video.select_one('.tgme_widget_message_video_thumb').attrs['style']
        vid['thumb'] = get_bg_image(thumb)
        vid['duration'] = video.select_one('.message_video_duration').text.strip()
        vid['src'] = video.select_one('.tgme_widget_message_video').attrs['src']
        post['video'] = vid

    text = msg.select_one('.js-message_text')
    if text is not None:
        post['text'] = re.sub(re.compile('<(?!br)(.*?)>'), '', str(text)).replace('<br/>', '\n')

    info = msg.select_one('.tgme_widget_message_info')
    if info is not None:
        post['date'] = info.select_one('time').attrs['datetime']
        views = info.select_one('.tgme_widget_message_views')
        if views is not None:
            post['views'] = views.text

    imgs = msg.select('.tgme_widget_message_photo_wrap')
    if len(imgs) != 0:
        images = [{'href': i.attrs['href'], 'url': get_bg_image(i.attrs['style'])} for i in imgs]
        post['images'] = images

    return post


def parse_posts(s: BeautifulSoup) -> list[dict]:
    msgs = s.select('.tgme_widget_message')
    return [parse_post(msg) for msg in msgs]


def get_bg_image(css: str) -> str:
    return cssutils.parseStyle(css)['background-image']\
        .replace('url(', '').replace(')', '')


def get_all_posts(channel: str):
    print('Updating...')

    s = BeautifulSoup(requests.get(f'https://t.me/s/{channel}').text, 'html.parser')
    posts = parse_posts(s)

    more = [e for e in s.select('.tme_messages_more') if 'data-before' in e.attrs]
    while len(more) != 0:
        url = 'https://t.me' + more[0].attrs['href']
        print(url)
        s = BeautifulSoup(requests.get(url).text, 'html.parser')
        new = parse_posts(s)
        posts += new
        posts.sort(key=lambda x: int(x['id']))
        more = [e for e in s.select('.tme_messages_more') if 'data-before' in e.attrs]
        print(f'{len(new)} additional posts parsed (Total {len(posts)})')

    return posts

