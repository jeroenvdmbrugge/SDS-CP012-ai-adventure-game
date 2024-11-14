import os
import logging
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

#print(os.environ.get("OPENAI_API_KEY")) # True of False

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a dungeon master and you will create a text based fantasy adventure game for a user to play and interact with using text. Generate a fantasy land and story for a short text based adventure game and describe it to the user. Ask them to pick between 3 different avatars: Wizard, archer, swordsman. For each avatar, give the user a short description of the abilities of each, health points, and the moves each one of them has."},
        {
            "role": "user",
            "content": "What is the game and what are the game rules?"
        }
    ]
)

print(completion.choices[0].message)