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

# Welcome message
print("Welcome to the Fantasy Adventure Game!")
print("You are embarking on a unique journey where your choices shape the story.")

# Initialize game summary
game_summary = {"actions": []}

while True:
    print("\nDescribe your next action or decision, and the Dungeon Master will guide your journey.")
    player_action = input("Enter your action (or type 'end' to conclude your adventure): ").strip()
    
    if player_action.lower() == "end":
        print("\nYou have chosen to end your journey.")
        print("Summarizing your adventure...\n")

        # Generate a game summary prompt
        prompt = (
            f"Summarize the adventure of a player who made the following actions: "
            f"{', '.join(game_summary['actions'])}. "
            f"Make the summary exciting, immersive, and reflective."
        )
        summary = get_response(prompt)
        print(summary)
        break

    if player_action:
        # Save action in summary
        game_summary["actions"].append(player_action)

        # Request model response based on action
        prompt = f"As the Dungeon Master, narrate what happens after the player decides to: {player_action}. Make it immersive and exciting."
        response = get_response(prompt)
        print(response)
    else:
        print("Please enter an action or type 'end' to conclude the game.")
