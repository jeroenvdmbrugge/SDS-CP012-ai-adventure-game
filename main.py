from routers.chat_openrouter import ChatOpenRouter
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import asyncio
import os
from utils.config import load_environment_variables, get_api_key
import logging
from pathlib import Path
from typing import List
from langchain.schema import BaseMessage

async def main():
    # Load environment variables
    load_environment_variables()
    
    # Read system prompt from markdown file
    prompt_path = Path("templates/system_prompt.md")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_content = f.read().strip()
    except FileNotFoundError:
        logging.error(f"Prompt file not found: {prompt_path}")
        raise
    
    # Initialize the AI storyteller with explicit API key
    storyteller = ChatOpenRouter(
        model_name="google/gemma-2-9b-it:free",
        openai_api_key=get_api_key('OPENROUTER_API_KEY')
    )
    
    # Initialize message history with LangChain message types directly
    messages : List[List[BaseMessage]] = [
        [
            SystemMessage(content=prompt_content),
            HumanMessage(content="Start a new adventure story")
        ]
    ]

    try:
        while True:
            # Generate story continuation
            response = await storyteller.agenerate_with_retry(messages=messages)
            story_text = response.generations[0][0].text
            print("\n" + story_text + "\n")
            
            # Add AI response to message history
            messages.append([AIMessage(content=story_text)])
            
            # Get player input
            user_input = input("What would you like to do? (or type 'quit' to end): ")
            
            if user_input.lower() == 'quit':
                print("\nThanks for playing!")
                break
            
            # Add user input to message history
            messages.append([HumanMessage(content=user_input)])
            
            # Maintain conversation history (keep last 6 messages to avoid token limits)
            if len(messages) > 6:
                messages = [messages[0]] + messages[-5:]  # Keep system prompt and last 5 messages
                
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error in main loop: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main()) 