# TelegramChanApi

This repo uses GitHub Pages and GitHub Actions to create an json API for a Telegram channel.

## Usage

1. Fork this repo
2. Change the channel ID in /src/github_actions.py
3. Run GitHub actions
4. Go to GitHub Pages settings and enable it, select /docs as the root directory.
5. Your channel json will be hosted at https://<username>.github.io/TelegramChanApi/posts.json

(The GitHub actions script will update the JSON once every two hours)

## Example

https://telegram-api.hydev.org/posts.json
