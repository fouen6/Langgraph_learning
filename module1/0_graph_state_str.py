from langgraph.graph import StateGraph, START, END 



def greeting(state:str)-> str:
    return state + "  welcome to Langgraph!"



builder = StateGraph(str)


# add nodes
builder.add_node("greeting",greeting)

# add edges
builder.add_edge(START, "greeting")
builder.add_edge("greeting",END)

graph = builder.compile()

# print(graph.invoke("hello, i am fouen6!"))