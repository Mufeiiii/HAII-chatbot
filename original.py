import openai
import streamlit as st

# set the model and api
st.title("Find Your Calm, One Day at a Time")
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# greetings
with st.chat_message("assistant"):
    st.write("It's nice to see you here! How's your day going?")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# react to user input
if prompt := st.chat_input("How's your day?"):
    
    # display user message in chat container
    with st.chat_message("user"):
        st.markdown(prompt)
    # add user messages to chat history
    st.session_state.messages.append({"role":"user","content":prompt})

    # generate gpt response
    with st.chat_message("assistant"):
        # variables for building the response
        message_placeholder = st.empty()
        full_response = ""
        # call the api in real-time
        for response in openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role":m["role"],"content":m["content"]}
                for m in st.session_state.messages
            ],
            # slowly get gpt response to simulate typing effect
            stream=True,
        ):
            # show the response with typing effect in the window
            delta_content = response.choices[0].delta.content
            if delta_content is not None:
                full_response += delta_content
                message_placeholder.markdown(full_response + "┃")
        
        # show the response one more time without typing effect
        message_placeholder.markdown(full_response)
    # add gpt response to message list
    st.session_state.messages.append({"role":"assistant","content":full_response})