from typing import List, Optional
from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
import logging
from .config import ChatConfig

class GameEngine:
    def __init__(self, config: ChatConfig):
        self.config = config
        self.messages: List[BaseMessage] = []
        self.storyteller = config.get_chat_provider()
        
        # Initialize chains
        self._setup_chains()
        
    def _setup_chains(self):
        """Setup the various processing chains"""
        # Character options chain
        character_prompt = ChatPromptTemplate.from_messages([
            ("system", self._load_prompt(self.config.system_prompt_path)),
            ("human", self._load_prompt("templates/character_setting_setup.md"))
        ])
        self.character_chain = character_prompt | self.storyteller | StrOutputParser()
        
        # Story continuation chain
        story_prompt = ChatPromptTemplate.from_messages([
            ("system", self._load_prompt(self.config.system_prompt_path)),
            ("human", "{user_input}")
        ])
        self.story_chain = story_prompt | self.storyteller | StrOutputParser()

    def _load_prompt(self, path: str) -> str:
        """Load prompt from file"""
        try:
            return Path(path).read_text(encoding="utf-8").strip()
        except FileNotFoundError as e:
            logging.error(f"Prompt file not found: {path}")
            raise

    def initialize_game(self, character_selection: Optional[str] = None):
        """Setup initial game state and prompts"""
        # Get character options using the character chain
        options_text = self.character_chain.invoke({})
        
        # Store initial messages
        self.messages = [
            SystemMessage(content=self._load_prompt(self.config.system_prompt_path)),
            HumanMessage(content=self._load_prompt("templates/character_setting_setup.md")),
            AIMessage(content=options_text)
        ]
        
        # If no character selection provided, just return the options
        if not character_selection:
            return {
                "options": options_text,
                "initial_story": ""
            }
        
        # Only proceed with story generation if character_selection isn't "Start the adventure!"
        if character_selection != "Start the adventure!":
            # Add character selection and start command to messages
            self.messages.extend([
                HumanMessage(content=character_selection),
                HumanMessage(content="Start the adventure with the selected character and setting!")
            ])
            
            # Generate initial story response
            initial_story = self.story_chain.invoke({
                "user_input": self.messages[-1].content
            })
            self.messages.append(AIMessage(content=initial_story))
            
            return {
                "options": options_text,
                "initial_story": initial_story
            }
        
        # If it's just the initial "Start the adventure!" command, return only options
        return {
            "options": options_text,
            "initial_story": ""
        }

    def process_turn(self, user_input: str) -> str:
        """Process a single game turn (UI version)"""
        try:
            # Add user input to messages
            self.messages.append(HumanMessage(content=user_input))
            
            # Generate story continuation
            story_text = self.story_chain.invoke({
                "user_input": self.messages[-1].content
            })
            
            # Add AI response to messages
            self.messages.append(AIMessage(content=story_text))
            
            # Maintain conversation history
            if len(self.messages) > self.config.max_history:
                self.messages = [self.messages[0]] + self.messages[-(self.config.max_history-1):]
            
            return story_text
            
        except Exception as e:
            logging.error(f"Error processing turn: {str(e)}", exc_info=True)
            raise

    async def run_game_loop(self):
        """Main game loop (Terminal version)"""
        try:
            # Initialize game
            game_init = self.initialize_game()
            print(game_init["options"])
            
            # Get character selection
            character_selection = input("Choose your character and setting: ")
            game_init = self.initialize_game(character_selection)
            print("\nStarting adventure...\n")
            print(game_init["initial_story"])
            
            while True:
                # Get player input
                user_input = input("\nWhat would you like to do? (or type 'quit' to end): ")
                
                if user_input.lower() == 'quit':
                    print("\nThanks for playing!")
                    break
                
                # Process turn and display result
                story_text = self.process_turn(user_input)
                print("\n" + story_text)
                
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"Error in game loop: {str(e)}", exc_info=True)