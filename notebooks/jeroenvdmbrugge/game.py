from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import random


class TextAdventureGame:
    def __init__(self, llm):
        self.llm = llm
        self.history = []  # To track the conversation history
        self.environment = None
        self.character = None
        self.objects = []
        self.locations = []
        self.location_descriptions = {}
        self.inventory = []
        self.turns = 0
        self.max_turns = 10

    def generate_environments(self):
        """Generate environments by sending a prompt to the model."""
        prompt = "Suggest three unique and creative environments for a text-based adventure game, with each environment described in one sentence."
        response = self.llm.invoke(input=prompt)
        environments = response.content.strip().split("\n")
        return [env.strip("0123456789). -") for env in environments if env.strip()]

    def generate_environment_description(self, environment):
        """Generate a detailed description for the chosen environment."""
        prompt = f"Describe the {environment} environment in more detail, including what challenges or adventures await the player there."
        response = self.llm.invoke(input=prompt)
        return response.content.strip()

    def generate_characters(self, environment):
        """Generate characters based on the environment."""
        prompt = f"Suggest three unique characters suitable for exploring the {environment} in a text-based adventure game. Provide each character name and a brief description."
        response = self.llm.invoke(input=prompt)
        characters = response.content.strip().split("\n")
        return [char.strip("0123456789). -") for char in characters if char.strip()]

    def generate_character_description(self, character):
        """Generate a detailed description for the chosen character."""
        prompt = f"Describe the character '{character}' in more detail, including their background, strengths, and any abilities they may have."
        response = self.llm.invoke(input=prompt)
        return response.content.strip()

    def generate_locations(self):
        """Generate locations based on the character and environment."""
        prompt = f"Suggest five unique locations and their descriptions suitable for a {self.character} exploring the {self.environment} in a text-based adventure game. Format each location as 'Location Name: Description'."
        response = self.llm.invoke(input=prompt)
        location_entries = response.content.strip().split("\n")
        for entry in location_entries:
            if ": " in entry:
                name, description = entry.split(": ", 1)
                self.locations.append(name.strip())
                self.location_descriptions[name.strip()] = description.strip()

    def generate_objects(self):
        """Generate objects based on the character and environment."""
        prompt = f"Suggest three unique and thematic objects that a {self.character} might need to find while exploring the {self.environment} in a text-based adventure game."
        response = self.llm.invoke(input=prompt)
        objects = response.content.strip().split("\n")
        return [obj.strip("- ") for obj in objects if obj.strip()]

    def add_to_history(self, player_input, system_output):
        """Add player and system responses to conversation history."""
        self.history.append(f"Player: {player_input}")
        self.history.append(f"System: {system_output}")

    def get_valid_input(self, prompt, valid_choices):
        """Allow substring matching for user input."""
        while True:
            response = input(prompt).strip()
            normalized_response = response.lower()

            matching_choices = [
                choice for choice in valid_choices if normalized_response in choice.lower()
            ]

            if matching_choices:
                return matching_choices[0]  # Return the first match
            else:
                print(f"Invalid choice: '{response}'. Please try again.")

    def choose_environment(self):
        """Let the user choose an environment."""
        print("The world is vast and full of possibilities. A few potential realms await you:")
        environments = self.generate_environments()

        # Print a concise list with environment names and short descriptions
        for env in environments:
            #first_sentence = env.split('.')[0]  # Get the first sentence by splitting at the first period
            print(f"- {env}")  # Display the full environment name and first sentence

        prompt = "Where will today's journey take you? "
        self.environment = self.get_valid_input(prompt, environments)

        # Once chosen, give a more detailed description
        detailed_description = self.generate_environment_description(self.environment)
        print(f"\n{detailed_description}")

        # Add to conversation history
        self.add_to_history("Environment chosen", self.environment)

    def choose_character(self):
        """Let the user choose a character."""
        print(f"\nAs you step into the {self.environment.split(':')[0]}, you'll meet these intriguing figures:")

        characters = self.generate_characters(self.environment)

        # Print a concise list with character names and one-sentence descriptions
        for char in characters:
            print(f"- {char} - {char[:60]}...")  # First 60 characters of the character description

        prompt = "Step into the shoes of a hero. Who are you? "
        self.character = self.get_valid_input(prompt, characters)

        # Once chosen, give a more detailed description of the character
        detailed_description = self.generate_character_description(self.character)
        print(f"\nYou chose '{self.character}'.\n{detailed_description}")

        # Add to conversation history
        self.add_to_history("Character chosen", self.character)

    def setup_game(self):
        """Set up the game based on environment and character."""
        print(f"\nYou are a {self.character} exploring the {self.environment}!")
        self.generate_locations()
        self.objects = self.generate_objects()

        self.object_locations = random.sample(self.locations, len(self.objects))
        print("The game begins! Your goal is to find the hidden objects.")

        # Add initial setup to conversation history
        self.add_to_history("Game setup", f"Locations: {self.locations}, Objects: {self.objects}")

    def player_turn(self):
        """Handle a single turn where the player selects a location."""
        print(f"\nTurn {self.turns + 1}/{self.max_turns}")
        print("Locations you can visit:")
        for loc in self.locations:
            print(f"- {loc}")

        prompt = "Where do you want to travel to next? "
        location = self.get_valid_input(prompt, self.locations)

        print(f"\nYou travel to {location}.")
        print(f"{self.location_descriptions[location]}")  # Show the description

        if location in self.object_locations:
            found_object = self.objects[self.object_locations.index(location)]
            self.inventory.append(found_object)
            self.object_locations.remove(location)
            print(f"You found {found_object}!")
        else:
            print("There's nothing here. Explore another location.")

        # Add turn data to history
        self.add_to_history(f"Turn {self.turns + 1} - Location chosen", location)

    def play_game(self):
        """Run the main game loop."""
        self.choose_environment()
        self.choose_character()
        self.setup_game()

        while self.turns < self.max_turns and len(self.inventory) < 3:
            self.player_turn()
            self.turns += 1

        if len(self.inventory) == 3:
            print("\nCongratulations! You found all the objects and won the game!")
        else:
            print("\nGame over! You ran out of turns.")

        print(f"You have gathered: {self.inventory}")


if __name__ == "__main__":
    load_dotenv()

    llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
    game = TextAdventureGame(llm)
    game.play_game()
