# TelegramChanApi

This repo uses GitHub Pages and GitHub Actions to create an json API for a Telegram channel.

## ⚠️ 302: MOVED PERMANENTLY ⚠️

This script is no longer maintained, and the reworked version is moved to: [one-among-us/TelegramBackup](https://github.com/one-among-us/TelegramBackup). You can also check out an example backup repo using the reworked version here: [blog-data](https://github.com/hykilpikonna/blog-data)

The reworked version supports many more features such as videos, animated stickers, gifs, custom emojis, polls, location/venue, and more. Please use that one instead.

## Usage

1. Fork this repo
2. Change the channel ID in /src/github_actions.py
3. Run GitHub actions
4. Go to GitHub Pages settings and enable it, select `gh-pages` branch.
5. Your channel json will be hosted at `https://<username>.github.io/TelegramChanApi/posts.json`

(The GitHub actions script will update the JSON once every two hours)

## Example

https://profile-api.hydev.org/posts.json

# Zotero API Localization

Additionally, this repo can be used to localize your Zotero publications. Just go to Settings > Secrets and put your Zotero user id into a secret named ZOTERO_USERID.
