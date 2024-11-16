from config import client
from prompts import scene_prompt

def test_scene_prompt(location, inventory):
    prompt_text = scene_prompt.format(location=location, inventory=inventory)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a text-based adventure game generator."},
            {"role": "user", "content": prompt_text},
        ],
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    location = "a dark forest with an ancient oak in the center"
    inventory = "a lantern, a sword, and a map"
    result = test_scene_prompt(location, inventory)
    print("Scene Description:")
    print(result)
