import streamlit as st

from streamlit_calendar import calendar

# st.set_page_config(page_title="Demo for streamlit-calendar", page_icon="📆")

# st.markdown(
#     "## Demo for [streamlit-calendar](https://github.com/im-perativa/streamlit-calendar) 📆"
# )

# st.markdown(
#     "[![](https://img.shields.io/github/stars/im-perativa/streamlit-calendar?style=social)](https://github.com/im-perativa/streamlit-calendar)"
# )

mode = "list"

events = [
    {
        "title": "Event 1",
        # "allDay" : false,
        "color": "#FF6C6C",
        "start": "2024-07-03",
        "end": "2024-07-03",
        "resourceId": "a",
    },
    {
        "title": "Event 2",
        "color": "#FFBD45",
        "start": "2024-08-01",
        "end": "2024-08-01",
        "resourceId": "b",
    },
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
calendar_resources = [
    {"id": "a", "building": "Building A", "title": "Room A"},
    {"id": "b", "building": "Building A", "title": "Room B"},
    {"id": "c", "building": "Building B", "title": "Room C"},
    {"id": "d", "building": "Building B", "title": "Room D"},
    {"id": "e", "building": "Building C", "title": "Room E"},
    {"id": "f", "building": "Building C", "title": "Room F"},
]

calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "resources": calendar_resources,
    "selectable": "true",
}

calendar_options = {
    **calendar_options,
    "initialDate": "2024-07-01",
    "initialView": "listMonth",
}

state = calendar(
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key=mode,
)

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

# st.write(state)

# st.markdown("## API reference")
# st.help(calendar)