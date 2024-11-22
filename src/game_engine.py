from typing import List
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

    def initialize_game(self):
        """Setup initial game state and prompts"""
        # Get character options using the character chain
        options_text = self.character_chain.invoke({})
        print("\n=== Character and Setting Options ===")
        print(options_text)
        
        # Store messages for history
        self.messages = [
            SystemMessage(content=self._load_prompt(self.config.system_prompt_path)),
            HumanMessage(content=self._load_prompt("templates/character_setting_setup.md")),
            AIMessage(content=options_text)
        ]
        
        # Get user selection
        user_selection = input("Please choose a character and setting from the options above: ")
        self.messages.extend([
            HumanMessage(content=user_selection),
            HumanMessage(content="Start the adventure with the selected character and setting!")
        ])

    async def run_game_loop(self):
        """Main game loop"""
        try:
            while True:
                # Generate story continuation using the story chain
                story_text = self.story_chain.invoke({
                    "user_input": self.messages[-1].content
                })
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