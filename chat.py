import streamlit as st
import wikipediaapi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Wikipedia API with user agent
user_agent = "StreamlitBot/1.0 (https://yourwebsite.com)"
wiki_wiki = wikipediaapi.Wikipedia('en', headers={'User-Agent': user_agent})

# Setting page title and header
st.set_page_config(page_title="Enhanced Wikipedia Chatbot", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Enhanced Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# Initialize conversation history and user memory
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {}

st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Reset conversation
if clear_button:
    st.session_state['messages'] = []
    st.session_state['user_info'] = {}

# Display previous messages
for message in st.session_state['messages']:
    role = message["role"]
    content = message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Knowledge base
knowledge_base = {
    "who is messi": "Lionel Messi is an Argentine professional footballer who plays as a forward for Inter Miami CF and the Argentina national team. He is considered one of the greatest football players of all time.",
    "what is the world city": "A world city, also known as a global city, is a city that is a primary node in the global economic network. Examples include New York City, London, and Tokyo."
}

# Chat input
prompt = st.text_input("You:")
if st.button("Send") and prompt:
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Include user-specific information in the prompt
    system_message = "You are a helpful assistant."
    if 'name' in st.session_state['user_info']:
        system_message += f" The user's name is {st.session_state['user_info']['name']}."

    # Check knowledge base first
    prompt_lower = prompt.lower()
    if prompt_lower in knowledge_base:
        ai_response = knowledge_base[prompt_lower]
    else:
        # Get AI response from Wikipedia
        def fetch_wikipedia_summary(query):
            page = wiki_wiki.page(query)
            if page.exists():
                return page.summary[:500]  # Limiting to 500 characters for brevity
            else:
                return "Sorry, I couldn't find any information on that topic."

        ai_response = fetch_wikipedia_summary(prompt)

    # Extract and store the user's name if mentioned
    if "my name is" in prompt_lower:
        name_start_index = prompt_lower.find("my name is") + len("my name is")
        name = prompt[name_start_index:].strip().split()[0]
        st.session_state['user_info']['name'] = name
        ai_response += f" Nice to meet you, {name}!"

    st.session_state['messages'].append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
