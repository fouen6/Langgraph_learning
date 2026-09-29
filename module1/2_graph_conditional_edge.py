from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Literal


#State
class State(TypedDict):
    graph_str:str

# noed
def node1(state:State)->State:
    return {"graph_str": state["graph_str"]+ "  welcome to langgraph!"}

def node2(state:State)->State:
    return {"graph_str": state["graph_str"]+ "  i am in node2!"}

def node3(state:State)->State:
    return {"graph_str": state["graph_str"]+ "  i am in node3!"}

# edges
def next_step(state:State)->Literal["node2","node3"]:

    state_str = state["graph_str"]
    array_state_str = state_str.split(" ")

    if array_state_str[0] == "Hello":
        return "node2"
    return "node3"


# putting together
builder = StateGraph(State)
builder.add_node("node1",node1)
builder.add_node("node2",node2)
builder.add_node("node3",node3)

builder.add_edge(START, "node1")
builder.add_conditional_edges("node1", next_step)
builder.add_edge("node2",END)
builder.add_edge("node3",END)

graph = builder.compile()