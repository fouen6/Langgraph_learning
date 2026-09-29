import os
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

model_llm = ChatOpenAI(model=os.getenv("LLM_MODEL_ID"),
api_key=os.getenv("LLM_API_KEY"),
base_url=os.getenv("LLM_BASE_URL"),
temperature = 0.7)

@tool
def mutiply(nb1:int, nb2:int)-> int:
    """this tool is used for mutiplying 2 numbers and returning product"""
    return nb1 * nb2

model_llm_with_tool = model_llm.bind_tools([mutiply])

def chat_with_tool(state:MessagesState)->MessagesState:
    return {"messages":[model_llm_with_tool.invoke(state["messages"])]}

builder = StateGraph(MessagesState)

builder.add_node("chat_with_tool",chat_with_tool)

builder.add_edge(START, "chat_with_tool")
builder.add_edge("chat_with_tool",END)

graph = builder.compile()