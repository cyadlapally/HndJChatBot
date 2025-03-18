import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

import os

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory()

if 'messages' not in st.session_state.keys:
    st.session_state.messages = [
        {"role": "bot", "content": "Hello! I am a chatbot. How can I help you?"}
    ]


llm = ChatOpenAI(model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo", 
                 openai_api_key = st.secrets["TOGETHER_API_KEY"] , ## use your key
                      openai_api_base = "https://api.together.xyz/v1"
)

conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Create user interface
st.title("🗣️ Conversational Chatbot")
st.subheader("㈻ Simple Chat Interface for LLMs by Build Fast with AI")


if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation.predict(input = prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history


