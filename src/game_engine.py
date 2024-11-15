from typing import List
from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage
from pathlib import Path
import logging
from .config import ChatConfig

class GameEngine:
    def __init__(self, config: ChatConfig):
        self.config = config
        self.messages: List[BaseMessage] = []
        self.storyteller = config.get_chat_provider()
        
    def initialize_game(self):
        """Setup initial game state and prompts"""
        self._load_prompts()
        self._get_character_options()
        self._get_user_selection()
        
    def _load_prompts(self):
        try:
            system_prompt = Path(self.config.system_prompt_path).read_text(encoding="utf-8").strip()
            character_setup = Path("templates/character_setting_setup.md").read_text(encoding="utf-8").strip()
            
            self.messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=character_setup)
            ]
        except FileNotFoundError as e:
            logging.error(f"Prompt file not found: {e.filename}")
            raise

    def _get_character_options(self):
        options_response = self.storyteller.invoke(self.messages)
        options_text = options_response.content
        print("\n=== Character and Setting Options ===")
        print(options_text)
        self.messages.append(AIMessage(content=options_text))

    def _get_user_selection(self):
        user_selection = input("Please choose a character and setting from the options above: ")
        self.messages.append(HumanMessage(content=user_selection))
        self.messages.append(HumanMessage(content="Start the adventure with the selected character and setting!"))

    async def run_game_loop(self):
        """Main game loop"""
        try:
            while True:
                # Generate story continuation
                response = self.storyteller.invoke(self.messages) 
                story_text = response.content
                print(story_text)
                
                self.messages.append(AIMessage(content=story_text))
                
                # Get player input
                user_input = input("What would you like to do? (or type 'quit' to end): ")
                
                if user_input.lower() == 'quit':
                    print("\nThanks for playing!")
                    break
                
                self.messages.append(HumanMessage(content=user_input))
                
                # Maintain conversation history
                if len(self.messages) > self.config.max_history:
                    self.messages = [self.messages[0]] + self.messages[-(self.config.max_history-1):]
        
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"Error in game loop: {str(e)}", exc_info=True) 