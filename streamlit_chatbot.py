## Reference: https://www.youtube.com/watch?app=desktop&v=sBhK-2K9bUc
## Tutorial & Documentation: https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
## API Guide: https://platform.openai.com/docs/guides/text-generation


import openai
import streamlit as st

# Set the model and API
st.title("Find Your Calm, One Day at a Time")
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history and implicit system prompt
if "messages" not in st.session_state:
    # Implicit system prompt guiding GPT on tone and response style
    st.session_state.messages = [
        {"role": "system", "content": "You are a supportive and empathetic assistant that helps users reflect on their emotions. Provide thoughtful, gentle, and positive responses that encourage self-reflection and emotional well-being."}
    ]

# Greetings
with st.chat_message("assistant"):
    st.write("It's nice to see you here! How's your day going?")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":  # Exclude the system message from the display
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How's your day?"):
    
    # Display user message in chat container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate GPT response
    with st.chat_message("assistant"):
        # Variables for building the response
        message_placeholder = st.empty()
        full_response = ""
        
        # Call the API in real-time
        for response in openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            # Stream GPT response to simulate typing effect
            stream=True,
        ):
            delta_content = response.choices[0].delta.content
            if delta_content:
                full_response += delta_content
                message_placeholder.markdown(full_response + "┃")
        
        # Show the response one more time without the typing effect
        message_placeholder.markdown(full_response)
    # Add GPT response to message history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
