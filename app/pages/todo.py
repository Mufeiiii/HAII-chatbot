import streamlit as st
import openai

if "to_do" in st.session_state:
    st.write(st.session_state.to_do)

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


with st.sidebar:
    st.markdown("### Quick Tools")
    st.write("If you want to generate the a potential to-do list, please press this button.")
    if st.button("Re-generate To-do"):
        # st.switch_page("todo.py")
        auto_prompt = "Can you help me generate a to-do list for targeting this issue?"

        # Display the auto-prompt in chat
        with st.chat_message("user"):
            st.markdown(auto_prompt)

        # Add auto-prompt to message history
        st.session_state.messages.append({"role": "user", "content": auto_prompt})

        # Generate GPT response for auto-prompt
        generate_gpt_response(st.session_state.messages)
    if st.button("Back to Chat"):
        st.switch_page("chat.py")