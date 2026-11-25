from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

load_dotenv()

model = init_chat_model("gemini-3.5-flash-lite", model_provider="google_genai")

system_prompt = SystemMessage("You are a friendly, helpful assistant.")

def call_model(state: MessagesState):
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

graph = StateGraph(MessagesState)
graph.add_node("model", call_model)
graph.add_edge(START, "model")

app = graph.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "chat-1"}}

print("Chatbot ready. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    result = app.invoke({"messages": [HumanMessage(user_input)]}, config)
    content = result["messages"][-1].content
    if isinstance(content, list):
        content = "".join(
            block.get("text", "") for block in content if isinstance(block, dict)
        )
    print("Bot:", content)