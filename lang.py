import os
import streamlit as st
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
import google.generativeai as genai
import requests
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

# --------------------
# Load environment vars
# --------------------
load_dotenv()
SERPER_API_KEY = "Y43841102b32b90e67d700ef5f24a85f5632ec7b8"
GOOGLE_API_KEY = "AIzaSyCzWmYUHD6i1rT6qWLpKVubDGpB4m8PDLg"

# --------------------
# Setup Gemini
# --------------------
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

def run_gemini(prompt: str) -> str:
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {e}"

# --------------------
# Serper Tool
# --------------------
def search_tool(query: str) -> str:
    try:
        url = "https://google.serper.dev/search"
        payload = {"q": query}
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        if "organic" in result and result["organic"]:
            top = result["organic"][0]
            return f"{top['title']}: {top['link']}\n{top['snippet']}"
        return "No results found."
    except Exception as e:
        return f"Serper Error or no results: {e}"

# --------------------
# LangGraph Flow
# --------------------
class GraphState(TypedDict):
    query: str
    search_result: str
    llm_response: str

def search_node(state: GraphState) -> GraphState:
    result = search_tool(state["query"])
    return {**state, "search_result": result}

def gemini_node(state: GraphState) -> GraphState:
    prompt = f"Use this info to answer the query:\nSearch:\n{state['search_result']}\n\nQuery:\n{state['query']}"
    response = run_gemini(prompt)
    return {**state, "llm_response": response}

def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node("search", search_node)
    builder.add_node("llm", gemini_node)
    builder.set_entry_point("search")
    builder.add_edge("search", "llm")
    builder.set_finish_point("llm")
    return builder.compile()

# --------------------
# Streamlit UI
# --------------------
st.set_page_config(page_title="Gemini LangGraph AI Agent", page_icon="🤖")
st.title("🔍 Gemini-Powered AI Agent")
st.caption("LangGraph + Serper.dev + Gemini via Streamlit")

query = st.text_input("Ask your question")

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

if st.button("Run Agent") and query:
    with st.spinner("Thinking..."):
        output = st.session_state.graph.invoke({"query": query})
        st.subheader("💬 Gemini's Answer")
        st.write(output["llm_response"])

        st.subheader("🔎 Search Result Used")
        st.code(output["search_result"])




# ─── TOOLS ─────────────────────────────────────────────────────────────────


# 🔎 Custom Tool: Serper Search
@tool
def search_web(query: str) -> str:
    """Searches Google using Serper API and returns the first result."""
    url = "https://google.serper.dev/search"
    payload = {"q": query}
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers).json()
        if "organic" in response and response["organic"]:
            r = response["organic"][0]
            return f"Title: {r['title']}\nLink: {r['link']}\nSnippet: {r['snippet']}"
        return "No results found."
    except Exception as e:
        return f"Search failed: {str(e)}"

# 🧠 Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    convert_system_message_to_human=True
)

# Bind Tools
llm_with_tools = llm.bind_tools([search_web])

# LangGraph State
def create_graph():
    builder = StateGraph(GraphState)
    builder.add_node("agent", llm_with_tools)
    builder.set_entry_point("agent")
    builder.add_edge("agent", END)
    return builder.compile()

graph = create_graph()

# 🌐 Streamlit UI
st.title("🧠 Gemini + LangGraph Agent with Web Search")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = msg.type.capitalize()
    st.markdown(f"**{role}:** {msg.content}")

user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input:
    # Run LangGraph
    result = graph.invoke({"query": user_input})
    st.markdown(f"**AI:** {result['llm_response']}")
    st.markdown(f"**Search Result:** {result['search_result']}")