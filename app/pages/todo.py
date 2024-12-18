import streamlit as st
import openai
from datetime import datetime
from prompt import CBPT_MEMORY
from prompt import advice_prompt

# if "to_do" in st.session_state:
#     st.write(st.session_state.to_do)

# Initialize chat history and implicit system prompt
if "messages" not in st.session_state:
    # Implicit system prompt guiding GPT on tone and response style
    st.session_state.messages = []

st.session_state.messages.append (
    {"role": "system", "content":  CBPT_MEMORY}
)

if "chat_summary" not in st.session_state:
    st.session_state.chat_summary = []
if "emoji_selections" not in st.session_state:
    st.session_state.emoji_selections = None  # Only one selection allowed
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""  # Only one selection allowed


    
def button_op():
    st.write("If you want to end or discard chat, please press the end-chat button.")
    with st.popover("End Chat"):
        if st.button("Save in Calendar"):
            # Generate a summary of the chat using GPT
            # chat_history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages if msg['role'] != "system"])
            summary_prompt = f"Summarize the users' events and feelings in no more than 20 words to capture key emotions and themes. BE CONCISE. Start every sentence with \"You\". DO NOT include any suggestions. Here is the chat history you want to summarize: \n\n{st.session_state.chat_history}."
            
            # summary_prompt = f"Based on our chat history, summarize my events and feelings in in no more than three sentences to capture key emotions and themes(please DON't include any suggestions or advice you give me)"
            
            # Call OpenAI API to get the summary
            try:
                response = openai.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        # {"role": "system", "content": "You are an assistant summarizing a chat for emotional reflection. "},
                        # {"role": "user", "content": summary_prompt}
                        {"role": "assistant", "content": summary_prompt}
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
            st.session_state.chat_summary.append({"second": second, "date": today_date, "time": current_time, "summary": summary, 
                                                     "emotions": st.session_state.emoji_selections, 
                                                     "to-do": st.session_state.to_do})
            # # Display the saved summary to the user
            # st.write(f"### Chat Summary for {today_date}")
            # st.markdown(summary)
            # st.success("Chat summary has been saved.")
            
            # Disable chatbot
            st.session_state.messages = []  # Clear chat history
            # st.session_state.chat_disabled = True
            st.switch_page("pages/calendar.py")
        if st.button("Discard Chat"):
            st.session_state.messages = []  # Clear chat history
            st.switch_page("chat.py")

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
        
        if "to_do" not in st.session_state:
            st.session_state.to_do = ""  # Initialize if not already in session state
            st.session_state.to_do = full_response

    # Add the assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

def new(messages):
    """
    Generates a GPT response based on the current chat history.
    Appends the response to the chat and displays it in the UI.
    """
    # Call the OpenAI API with the current messages
    response = openai.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]} for m in messages
        ]
    )
    
    # Get the full response content
    full_response = response.choices[0].message.content

    # # Display the response in the chat container
    # with st.chat_message("assistant"):
    #     st.markdown(full_response)

    # Save the response as a to-do list or assistant response
    if "to_do" not in st.session_state:
        st.session_state.to_do = ""  # Initialize if not already in session state
    st.session_state.to_do = full_response

    # Add the assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})


with st.sidebar:
    st.markdown("### Quick Tools")
    st.write("If you want to generate the a potential to-do list, please press this button.")
    if st.button("Re-generate To-do"):
        # st.switch_page("todo.py")
        user_input = "Can you help me generate a to-do list for targeting this issue?"

        # Display the auto-prompt in chat
        # with st.chat_message("user"):
        #     st.markdown(auto_prompt)

        # Add auto-prompt to message history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append( {"role": "assistant", "content": advice_prompt})

        # Generate GPT response for auto-prompt
        new(st.session_state.messages)
    if st.button("Back to Chat"):
        st.switch_page("chat.py")
    button_op()
    
        
        
def generate_todo():      
    # auto_prompt = "Can you help me generate a to-do list for targeting this issue?"

    # # Display the auto-prompt in chat
    # with st.chat_message("user"):
    #     st.markdown(auto_prompt)

    # Add auto-prompt to message history
    # st.session_state.messages.append({"role": "user", "content": auto_prompt})
    user_input = "Can you help me generate a to-do list for targeting this issue?"
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append( {"role": "assistant", "content": advice_prompt})

    # Generate GPT response for auto-prompt
    generate_gpt_response(st.session_state.messages)
    
generate_todo()
# st.write(st.session_state.chat_summary)
# st.write(st.session_state.to_do)