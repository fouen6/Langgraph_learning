from langgraph.graph import StateGraph,START, END
from typing_extensions import TypedDict

#State
class State(TypedDict):
    graph_str:str

#node
def greeting(state:State)->State:
    return {"graph_str":state["graph_str"]+" welcome to langgraph!"}

# edges


#putting togther
builder = StateGraph(State)

builder.add_node("greeting",greeting)

builder.add_edge(START,"greeting")
builder.add_edge("greeting",END)

graph = builder.compile()