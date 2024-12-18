import streamlit as st

from streamlit_calendar import calendar
from menu import menu

# st.set_page_config(page_title="Demo for streamlit-calendar", page_icon="📆")

# st.markdown(
#     "## Demo for [streamlit-calendar](https://github.com/im-perativa/streamlit-calendar) 📆"
# )

# st.markdown(
#     "[![](https://img.shields.io/github/stars/im-perativa/streamlit-calendar?style=social)](https://github.com/im-perativa/streamlit-calendar)"
# )

menu()

if "chat_summary" not in st.session_state:
    st.session_state.chat_summary = []

custom_css = """
/* Hide the dot for events with the 'no-dot' class */
.fc-event.no-dot .fc-event-dot {
    display: none !important; /* Use !important to override default styles */
}

/* Add the red dot for events with the 'red-dot' class */
.fc-event.red-dot .fc-event-dot {
    display: inline-block; /* Ensure dot is shown */
}

/* Hide all-day labels in list views */
.fc-list-event-time {
    display: none;
}

/* Customize the event title */
.fc-list-event-title {
    font-weight: regular;
    color: #333;
}

/* Adjust the toolbar title size */
.fc-toolbar-title {
    font-size: 1.5rem;
}

/* Add custom event styling */
.fc-event {
    background-color: #FFFFFF;
    border-radius: 5px;
    padding: 5px;
}

"""

# /* Hide the red dot in front of events */
# .fc-list-event-dot {
#     display: none;
# }


if "chat_summary" not in st.session_state:
    st.session_state.chat_summary = []

mode = "list"

example_string = [
    "Emotions: 😊",
    "Summary: The user expressed feeling overwhelmed with a lot of homework to do. They received support and encouragement to take breaks, prioritize tasks, and believe in their ability to tackle their workload. The key emotions and themes are stress, determination, support, and resilience.",
    "To-Do: 'Be patient'"
]

if "events" not in st.session_state:
    st.session_state.events = []

st.session_state.events = [
        {
            "title": "Event 3",
            "color": "#FF4B4B",
            "start": "2024-07-20",
            "end": "2024-07-20",
            "resourceId": "c",
        },
        {
            "title": "Event 4",
            "color": "#FF6C6C",
            "start": "2024-07-23",
            "end": "2024-07-23",
            "resourceId": "d",
        },
    ]

for index, chat in enumerate(st.session_state.chat_summary):
    st.session_state["events"].append({
        "title": chat["emotions"][0]+" "+ chat["emotions"][1]+", "+chat["time"],
        "color": "#FF6C6C",
        "start": chat["date"]+"T"+chat["time"]+chat["second"],
    })
    st.session_state["events"].append({
        "title": "Chat Summary: " + chat["summary"],
        "color": "#FFFFFF",
        "start": chat["date"]+"T"+chat["time"]+chat["second"],

    })
    if chat["to-do"]!="": 
        st.session_state["events"].append({
            "title": "Your To-Do List: "+ chat["to-do"],
            "color": "#FFFFFF",
            "start": chat["date"]+"T"+chat["time"]+chat["second"],
        })

st.session_state["events"].sort(key=lambda x: x.get("order", 0))


calendar_options = {
    "editable": "true",
    "navLinks": "true",
    # "resources": calendar_resources,
    "selectable": "true",
}

calendar_options = {
    **calendar_options,
    "initialDate": "2024-10-01",
    "initialView": "listMonth",
}

state = calendar(
    events=st.session_state.events,
    options=calendar_options,
    custom_css=custom_css,
    key=mode,
)

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

# st.write(state)

# st.markdown("## API reference")
# st.help(calendar)



# st.write(st.session_state.chat_summary)