import os
from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
from typing import Literal, NotRequired
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# State
class State(TypedDict):
    graph_int: NotRequired[int]
    graph_str: str

model_llm = ChatOpenAI(model=os.getenv("LLM_MODEL_ID"),
api_key=os.getenv("LLM_API_KEY"),
base_url=os.getenv("LLM_BASE_URL"),
temperature = 0.7)


# node
def node1(state:State)->State:
    model_response = model_llm.invoke("choose between 2 or 3. reply only with a number")

    if isinstance(int(model_response.content),int):
        return {
            "graph_int":int(model_response.content),
            "graph_str": state["graph_str"]+ " passed by node1"
        }
    return {
            "graph_int":0,
            "graph_str": state["graph_str"]+ " passed by node1"
        }


def node2(state:State)->State:
    return {
            "graph_int":state["graph_int"],
            "graph_str": state["graph_str"]+ " passed by node2"
        }

def node3(state:State)->State:
    return {
            "graph_int":state["graph_int"],
            "graph_str": state["graph_str"]+ " passed by node3"
        }

# edge
def next_step(state:State)->Literal["node2","node3",END]:
    if state["graph_int"] == 2:
        return "node2"
    elif state["graph_int"] == 3:
        return "node3"
    else :
        return END

# putting together

bulider = StateGraph(State)
bulider.add_node("node1",node1)
bulider.add_node("node2",node2)
bulider.add_node("node3",node3)

bulider.add_edge(START,"node1")
bulider.add_conditional_edges("node1",next_step)
bulider.add_edge("node2",END)
bulider.add_edge("node3",END)

graph = bulider.compile()
