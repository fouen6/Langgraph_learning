import os
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.messages import SystemMessage
from typing import Literal

load_dotenv

model_llm = ChatOpenAI(model=os.getenv("LLM_MODEL_ID"),
api_key=os.getenv("LLM_API_KEY"),
base_url=os.getenv("LLM_BASE_URL"),
temperature = 0.7)

@tool
def mutiply(nb1:int, nb2:int)-> int:
    """this tool return the multiplication of 2 numbers"""
    return nb1 * nb2

@tool
def addition(nb1:int, nb2:int)-> int:
    """this tool return the sum of 2 numbers"""
    return nb1 + nb2

@tool
def subtraction(nb1:int, nb2:int)-> int:
    """this tool return the subtraction of 2 numbers"""
    return nb1 - nb2

model_llm_with_tools = model_llm.bind_tools([mutiply,addition,subtraction])

system_message = SystemMessage(content="you are a helpful math teacher")

def chat_with_tools(state:MessagesState)->MessagesState:
    return {"messages":[model_llm_with_tools.invoke(state["messages"]+[system_message])]}



builder = StateGraph(MessagesState)

builder.add_node("chat_with_tools",chat_with_tools)
builder.add_node("tools",ToolNode([mutiply,addition,subtraction]))

builder.add_edge(START, "chat_with_tools")
builder.add_conditional_edges("chat_with_tools",tools_condition)
# builder.add_edge("tools",END)
builder.add_edge("tools","chat_with_tools")
graph = builder.compile()
