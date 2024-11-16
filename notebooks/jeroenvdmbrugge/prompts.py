from langchain.prompts import PromptTemplate

scene_prompt = PromptTemplate(
    input_variables=["location", "inventory"],
    template="""
    You are in {location}. Your inventory includes: {inventory}.
    Describe the scene and suggest 3 possible actions.
    """
)