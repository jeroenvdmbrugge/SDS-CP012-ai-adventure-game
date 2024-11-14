
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")

response = model.invoke("I would like you to build a text based adventure game with a quest which will proceed by having a conversation with me.")

print(response.content)


