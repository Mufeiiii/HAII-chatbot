## Reference: https://www.youtube.com/watch?app=desktop&v=sBhK-2K9bUc
## Tutorial & Documentation: https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
## API Guide: https://platform.openai.com/docs/guides/text-generation


import openai
import streamlit as st
from datetime import datetime
from prompt import REFLECTION_MEMORY
# from prompt import summary_prompt

st.set_option("client.showSidebarNavigation", False)

# Set the model and API
st.title("Share your emotion with me")


def menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("chat.py", label="Chat")
    st.sidebar.page_link("pages/calendar.py", label="Calendar")

menu()


# openai.api_key = "r8_JwpVSPywK4stcBSjUEi4I5CO0HdSe692ZzAxm"
openai.api_key = "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"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history and implicit system prompt
if "messages" not in st.session_state:
    # Implicit system prompt guiding GPT on tone and response style
    st.session_state.messages = [
        {"role": "system", "content": REFLECTION_MEMORY}
    ]
if "chat_summary" not in st.session_state:
    st.session_state.chat_summary = []

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

# Initialize a dictionary to track the selection
if "emoji_selections" not in st.session_state:
    st.session_state.emoji_selections = None  # Only one selection allowed

# Render the radio button group for emoji selection (only one can be selected)
selected_emoji = st.radio(
    "Select your mood:",
    options=[(emoji, description) for emoji, description in emoji_options.items()],
    format_func=lambda x: f"{x[0]} - {x[1]}",  # Format the display as emoji and description
    key="emoji_selection"
)
st.session_state.emoji_selections = selected_emoji

# Submit button to finalize selection
if st.button("Submit"):
    if selected_emoji:
        # Combine the selected emoji with the description
        selected_emoji_emoji, selected_emoji_description = selected_emoji
        mood_summary = f"{selected_emoji_emoji} ({selected_emoji_description})"
        user_input = f"My current mood is: {mood_summary}."

        # Append user input to chat history (if needed)
        # st.session_state.messages.append({"role": "user", "content": user_input})

        # Reset emoji selection
        st.session_state.emoji_selections = None

        # Optionally, display the selected mood
        st.write(f"You selected: {mood_summary}")
    else:
        st.warning("Please select a mood before submitting!")

# Greetings
with st.chat_message("assistant"):
    st.write("How are you feeling today, is there anything that I can help you with?")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":  # Exclude the system message from the display
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Function to generate GPT response
def generate_gpt_response(messages):
    """
    Generates a GPT response based on the current chat history.
    Appends the response to the chat and displays it in the UI.
    """
    with st.chat_message("assistant"):
        # Placeholder for the response
        message_placeholder = st.empty()
        full_response = ""

        # Call the API with the current messages
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

        # Finalize the response display
        message_placeholder.markdown(full_response)

    # Add the assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":  # Exclude the system message from display
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input from chat_input
if prompt := st.chat_input("How's your day?"):
    # Display user message in chat container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user input to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate GPT response for user input
    generate_gpt_response(st.session_state.messages)

def button_op():
    with st.popover("End Chat"):
        if st.button("Save in Calendar"):
            # Generate a summary of the chat using GPT
            chat_history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages if msg['role'] != "system"])
            summary_prompt = f"Summarize the users' events and feelings in no more than three sentences to capture key emotions and themes:\n\n{chat_history}"
            
            # Call OpenAI API to get the summary
            try:
                response = openai.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": "system", "content": "You are an assistant summarizing a chat for emotional reflection."},
                        {"role": "user", "content": summary_prompt}
                        # {"role": "assistant", "content": summary_prompt}
                    ]
                )
                summary = response.choices[0].message.content
                # summary = response["choices"][0]["message"]["content"]
            except Exception as e:
                st.error(f"Error generating summary: {e}")
                summary = "Error: Could not generate summary."
            # Save the summary with today's date in session state
            today_date = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M") 
            second = datetime.now().strftime(":%S") 
            st.session_state.chat_summary.append({"second": second, "date": today_date, "time": current_time, "summary": summary, "emotions": selected_emoji, "to-do": ""})
            # # Display the saved summary to the user
            # st.write(f"### Chat Summary for {today_date}")
            # st.markdown(summary)
            # st.success("Chat summary has been saved.")
            
            # Disable chatbot
            st.session_state.messages = []  # Clear chat history
            # st.session_state.chat_disabled = True
            st.switch_page("pages/calendar.py")
            st.rerun()
        if st.button("Discard Chat"):
            st.session_state.messages = []  # Clear chat history
            st.rerun()


# Add the "Generate To-do" button in the sidebar
with st.sidebar:
    st.markdown("### Quick Tools")
    st.write("If you want to generate the a potential to-do list, please press this button.")
    if st.button("Generate To-do"):
        st.switch_page("pages/todo.py")
        
    button_op()

st.write(st.session_state.chat_summary)
            