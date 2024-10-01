from __future__ import annotations

from pathlib import Path

import openai
import rio

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "<placeholder>")


# Instruct the developer to replace the placeholder key if they haven't done so
# yet. Feel free to delete this code if you've already replaced the key.

if OPENAI_API_KEY == "<placeholder>":
    message = """
This template requires an OpenAI API key to work

You can get your API key from [OpenAI's website](https://platform.openai.com/api-keys
Make sure to enter your key into the `__init__.py` file before trying to run the project
""".strip()

    print(message)
    raise RuntimeError(message)


def on_app_start(app: rio.App):
    # Create the OpenAI client and attach it to the app
    app.default_attachments.append(openai.AsyncOpenAI(api_key=OPENAI_API_KEY))


# Define a theme for Rio to use.
#
# You can modify the colors here to adapt the appearance of your app or website.
# The most important parameters are listed, but more are available! You can find
# them all in the docs
#
# https://rio.dev/docs/api/theme
theme = rio.Theme.from_colors(
    primary_color=rio.Color.from_hex("01dffdff"),
    secondary_color=rio.Color.from_hex("0083ffff"),
    mode="light",
)


# Create the Rio app
app = rio.App(
    name='ragout-ui',
    # This function will be called once the app is ready.
    #
    # `rio run` will also call it again each time the app is reloaded.
    on_app_start=on_app_start,
    theme=theme,
    assets_dir=Path(__file__).parent / "assets",
)
