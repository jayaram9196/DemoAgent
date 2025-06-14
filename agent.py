from google.adk.agents import Agent, LlmAgent, SequentialAgent, ParallelAgent

from google.adk.models.lite_llm import LiteLlm

from textblob import TextBlob

MODEL = LiteLlm(model="groq/llma3-8b-8192")

def get_sentiment(text:str):
    sentiment = TextBlob(text).sentiment
    return sentiment.polarity


#root agent: must 

root_agent  = Agent(
    name="text_analysis_agent",

    model = MODEL,

    description=(
        "Agent to analyse a given text"
    ),
    instruction=(
        "You are a text analyst agent with ability to analyse a given text and also to provide the sentimnet in the text"
    ),
    tools=[get_sentiment],
)