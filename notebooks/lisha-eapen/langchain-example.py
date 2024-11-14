
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")

response = model.invoke("I would like you to build a text based adventure game with a quest which will proceed by having a conversation with me.")

print(response.content)

def get_response(user_input):
    response = model.invoke(user_input)
    if response.status_code == 200:
      print(response.status_code)
      result = response.json()
      print(result)
      # Parse the response to get generated text
      for response_dict in result:
        print(response_dict)
        return response_dict["generated_text"]
    else:
        print("Error:", response.status_code, response.text)
        return "Error generating response."

# Console-based game loop
def play_game():
    #print("Welcome to the DialoGPT Adventure Game!")
    #user_input = "start"  # initial input to start the game

    while True:

        # Get the next user input
        user_input = input("What action would you like to take? (type 'quit' to exit) ")
        if user_input.lower() == "quit":
            print("Thanks for playing! Goodbye.")
            break
        else:
            response = get_response(user_input.lower())
            print("Adventure Game Response:", response)

# Start the game
play_game()


