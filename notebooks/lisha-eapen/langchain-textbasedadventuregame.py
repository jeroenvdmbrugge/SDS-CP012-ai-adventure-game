from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")

# Function to interact with the model
def get_response(prompt):
    response = model.invoke(prompt)
    return response.content

# Function to show avatar choices with high moral standards and fantasy abilities
def show_avatar_choices():
    return """
Choose your noble avatar, each committed to learning, aiding others, and rejuvenating the spirit:

1. **The Guardian Knight** 🛡️: A hero of virtue, using bravery to protect others and nurture harmony.
   - Skills: Swordsmanship, meditation, and motivational guidance.

2. **The Enchanted Sage** 🌌: A wise spellcaster, helping others with knowledge and balanced wisdom.
   - Skills: Magic spells, botanical knowledge, and storytelling.

3. **The Wanderer of Light** 🌄: A skilled healer and traveler, cherishing rest and reflection.
   - Skills: Healing arts, nature lore, and empathy.

Type "1" for Guardian Knight, "2" for Enchanted Sage, or "3" for Wanderer of Light to choose your avatar.
"""

# Track game progress for summary
game_summary = {"avatar": "", "actions": []}

# Function to show age group choices
def show_age_group_choices():
    return """
Choose your age group to customize your adventure experience:

1. **Child** 🌈: Lighthearted, with fun learning and playful elements.
2. **Adolescent** ⚔️: Exciting, with action, meaningful interactions, and skill-building.
3. **Adult** 📜: Inspiring, with deeper reflection, noble decisions, and personal growth.

Type "1" for Child, "2" for Adolescent, or "3" for Adult to choose your age group.
"""

# Function to display choices based on the avatar and fantasy elements
def display_choices(avatar):
    choices = {
        "Guardian Knight": {
            "Play": "Practice your sword skills in a friendly duel with a sparring partner.",
            "Others": "Help villagers defend their town against a mysterious shadow.",
            "Down Time": "Meditate under a sacred tree to rejuvenate your mind and body."
        },
        "Enchanted Sage": {
            "Play": "Experiment with new spells to create enchanting lights and sounds.",
            "Others": "Share herbal remedies with a nearby village to heal the sick.",
            "Down Time": "Spend quiet time in a hidden forest glade, listening to birds."
        },
        "Wanderer of Light": {
            "Play": "Learn a new tune on your flute, filling the air with calming music.",
            "Others": "Heal a weary traveler, restoring their energy and spirit.",
            "Down Time": "Rest by a shimmering lake, watching reflections in the water."
        }
    }
    options = choices[avatar]
    options_text = "\n".join([f"{i + 1}. {option}: {description}" for i, (option, description) in enumerate(options.items())])
    return f"As the {avatar}, you may choose a path of:\n{options_text}\nOr type 'change' to switch your avatar, or 'end' to end the game."

# Start the game with age group selection
print("Welcome to the Fantasy Adventure Game!")
print(show_age_group_choices())

age_choice = None
while age_choice not in ["1", "2", "3"]:
    age_choice = input("Choose your age group (1, 2, or 3): ").strip()
    if age_choice not in ["1", "2", "3"]:
        print("Invalid choice. Please enter 1, 2, or 3.")

if age_choice == "1":
    age_group = "Child"
    tone = "lighthearted and playful"
elif age_choice == "2":
    age_group = "Adolescent"
    tone = "exciting and skill-building"
elif age_choice == "3":
    age_group = "Adult"
    tone = "inspiring and reflective"

print("\nNow, choose your avatar.")
print(show_avatar_choices())

avatar_choice = None
while avatar_choice not in ["1", "2", "3"]:
    avatar_choice = input("Choose your avatar (1, 2, or 3): ").strip()
    if avatar_choice not in ["1", "2", "3"]:
        print("Invalid choice. Please enter 1, 2, or 3.")

if avatar_choice == "1":
    avatar = "Guardian Knight"
elif avatar_choice == "2":
    avatar = "Enchanted Sage"
elif avatar_choice == "3":
    avatar = "Wanderer of Light"

# Save avatar choice in summary
game_summary["avatar"] = avatar

print(f"\nYou have chosen the {avatar}! As a {age_group}, your adventure will be {tone}. Let's begin!\n")

while True:
    print(display_choices(avatar))
    player_action = input("Enter your choice (1, 2, or 3), 'change' to switch avatar, or 'end' to end the game: ").strip().lower()
    
    if player_action == "change":
        print("\nYou have chosen to change your avatar.")
        print(show_avatar_choices())
        
        new_choice = None
        while new_choice not in ["1", "2", "3"]:
            new_choice = input("Choose your new avatar (1, 2, or 3): ").strip()
            if new_choice not in ["1", "2", "3"]:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        if new_choice == "1":
            avatar = "Guardian Knight"
        elif new_choice == "2":
            avatar = "Enchanted Sage"
        elif new_choice == "3":
            avatar = "Wanderer of Light"
        
        game_summary["avatar"] = avatar
        print(f"\nYou have switched to the {avatar}. Let’s continue the journey with renewed purpose!\n")
        continue

    elif player_action == "end":
        print("\nYou have chosen to end your journey.")
        print("Summarizing your noble adventure...\n")

        # Generate a game summary prompt
        prompt = f"Summarize the adventure of a player who chose the {game_summary['avatar']}, taking actions that included: " + ", ".join(game_summary["actions"]) + ". Make the summary noble, fun, and reflective."
        summary = get_response(prompt)
        print(summary)
        break

    # Map player input to action descriptions
    if player_action == "1":
        action_description = display_choices(avatar).split('\n')[1].split(': ')[1]
    elif player_action == "2":
        action_description = display_choices(avatar).split('\n')[2].split(': ')[1]
    elif player_action == "3":
        action_description = display_choices(avatar).split('\n')[3].split(': ')[1]
    else:
        print("Invalid choice. Please enter 1, 2, 3, 'change', or 'end'.")
        continue

    # Save action in summary
    game_summary["actions"].append(action_description)

    # Request model response based on action
    prompt = f"As a {avatar} in a {tone} setting, you choose to {action_description}. What happens next?"
    response = get_response(prompt)
    print(response)
