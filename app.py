import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

load_dotenv()

st.set_page_config(page_title="My LLM Chatbot", page_icon="💬")
st.title("💬 My LLM Chatbot")


@st.cache_resource
def build_app():
    model = init_chat_model("gemini-3.5-flash-lite", model_provider="google_genai")
    system_prompt = SystemMessage("You are a friendly, helpful assistant.")

    def call_model(state: MessagesState):
        response = model.invoke([system_prompt] + state["messages"])
        return {"messages": [response]}

    graph = StateGraph(MessagesState)
    graph.add_node("model", call_model)
    graph.add_edge(START, "model")
    return graph.compile(checkpointer=MemorySaver())


app = build_app()


def to_text(content):
    if isinstance(content, list):
        return "".join(
            block.get("text", "") for block in content if isinstance(block, dict)
        )
    return content


# Each browser session gets its own conversation
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    if st.button("New chat"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

# Show earlier messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Handle a new message
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                result = app.invoke({"messages": [HumanMessage(prompt)]}, config)
                reply = to_text(result["messages"][-1].content)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Something went wrong: {e}")