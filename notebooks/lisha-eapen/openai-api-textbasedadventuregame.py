from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI()

# Function to interact with the model
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can change the model if necessary
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message

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

print(f"\nYou have chosen the {avatar}! As a {age_group}, your adventure will be {tone}. Let's begin!\n")

# List to track user actions for summary
action_history = []

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
        
        print(f"\nYou have switched to the {avatar}. Let’s continue the journey with renewed purpose!\n")
        continue

    elif player_action == "end":
        # Generate summary of the adventure
        summary_prompt = f"Summarize the journey of a noble {avatar} in a {tone} adventure who took actions such as: {', '.join(action_history)}."
        summary = get_response(summary_prompt)
        print(f"\nYou have chosen to end your journey as the {avatar}.")
        print("Here is a summary of your adventure:\n")
        print(summary)
        print("\nThank you for playing!")
        break

    # Map player input to a descriptive path based on fantasy elements
    if player_action == "1":
        action_description = display_choices(avatar).split('\n')[1].split(': ')[1]
    elif player_action == "2":
        action_description = display_choices(avatar).split('\n')[2].split(': ')[1]
    elif player_action == "3":
        action_description = display_choices(avatar).split('\n')[3].split(': ')[1]
    else:
        print("Invalid choice. Please enter 1, 2, 3, 'change', or 'end'.")
        continue

    # Add the action description to the action history for summary
    action_history.append(action_description)
    
    prompt = f"As a {avatar} in a {tone} setting, you choose to {action_description}. What happens next?"

    # Get and print the response
    response = get_response(prompt)
    print(response)

    # End if response indicates the game is complete
    if "The End" in response or "Game Over" in response:
        print("Thank you for playing!")
        break
    
    print("\nWhat would you like to do next?")

