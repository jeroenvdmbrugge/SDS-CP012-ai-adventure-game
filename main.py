import asyncio
from utils.utils import load_environment_variables
from src.config import ChatConfig, ChatProvider
from src.game_engine import GameEngine

async def main():
    # Load environment variables
    load_environment_variables()
    
    # Initialize configuration
    config = ChatConfig(
        provider=ChatProvider.OPENAI, # can choose between OPENAI and OPENROUTER 
        system_prompt_path="templates/system_prompt.md",
        max_history=10
    )
    
    # Initialize and run game
    game = GameEngine(config)
    game.initialize_game()
    await game.run_game_loop()

if __name__ == "__main__":
    asyncio.run(main())