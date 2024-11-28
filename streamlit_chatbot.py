## Reference: https://www.youtube.com/watch?app=desktop&v=sBhK-2K9bUc
## Tutorial & Documentation: https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
## API Guide: https://platform.openai.com/docs/guides/text-generation


import openai
import streamlit as st

# Set the model and API
st.title("Find Your Calm, One Day at a Time")
openai.api_key = "r8_JwpVSPywK4stcBSjUEi4I5CO0HdSe692ZzAxm"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history and implicit system prompt
if "messages" not in st.session_state:
    # Implicit system prompt guiding GPT on tone and response style
    st.session_state.messages = [
        {"role": "system", "content": "You are a supportive and empathetic assistant that helps users reflect on their emotions. Provide thoughtful, gentle, and positive responses that encourage self-reflection and emotional well-being."}
    ]


# Emoji selection
st.write("How are you feeling right now? Select an emoji that resonates with your mood:")

# Define the emoji options
emoji_options = {
    "😊": "Happy",
    "😔": "Sad",
    "😡": "Angry",
    "😨": "Anxious",
    "😐": "Neutral",
    "🎉": "Excited"
}

# Initialize a dictionary to track selections
if "emoji_selections" not in st.session_state:
    st.session_state.emoji_selections = {emoji: False for emoji in emoji_options}

# Inject custom CSS for a grid layout
st.markdown(
    """
    <style>
    .emoji-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 20px 0;
    }
    .emoji-item {
        display: flex;
        align-items: center;
        padding: 5px;
        border: 1px solid lightgray;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }
    .emoji-item:hover {
        background-color: #f0f8ff;
    }
    .emoji-label {
        margin-left: 10px;
        font-size: 16px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Render checkboxes in a three-column grid
st.markdown('<div class="emoji-grid">', unsafe_allow_html=True)
for emoji, description in emoji_options.items():
    # Render each emoji with a checkbox
    selected = st.checkbox(f"{emoji} {description}", key=f"emoji_{emoji}")
    st.session_state.emoji_selections[emoji] = selected
st.markdown('</div>', unsafe_allow_html=True)

# Submit button to finalize selection
if st.button("Submit"):
    selected_emojis = [
        (emoji, emoji_options[emoji])
        for emoji, selected in st.session_state.emoji_selections.items()
        if selected
    ]

    if selected_emojis:
        # Display
        # st.write("You selected the following moods:")
        # for emoji, description in selected_emojis:
        #     st.write(f"{emoji} - {description}")

        # Combine selections into a single string for the assistant
        mood_summary = ", ".join([f"{emoji} ({description})" for emoji, description in selected_emojis])
        user_input = f"My current moods are: {mood_summary}."

        # Append user input to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Reset emoji selections
        st.session_state.emoji_selections = {emoji: False for emoji in emoji_options}

    else:
        st.warning("Please select at least one mood before submitting!")

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
