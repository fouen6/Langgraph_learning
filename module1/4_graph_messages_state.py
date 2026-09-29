import os
from langgraph.graph import START, END, StateGraph, MessagesState
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from typing import List, Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

# State

# class MessagesState(TypedDict):
#     messages: Annotated[List[AnyMessage], add_messages]

model_llm = ChatOpenAI(model=os.getenv("LLM_MODEL_ID"),
api_key=os.getenv("LLM_API_KEY"),
base_url=os.getenv("LLM_BASE_URL"),
temperature = 0.7)


def chat(state:MessagesState)->MessagesState:
    return {"messages":[model_llm.invoke(state["messages"])]}



bulider = StateGraph(MessagesState)

bulider.add_node("chat",chat)

bulider.add_edge(START, "chat")
bulider.add_edge("chat", END)

graph = bulider.compile()

