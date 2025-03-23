import streamlit as st
from datetime import datetime, timedelta
from scheduler import schedule_tasks
from chatbot import get_ai_feedback, chat_with_ai

def show_time_management_page():
    # ✅ Safely initialize session state variables
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = []

    if "completed_tasks" not in st.session_state:
        st.session_state["completed_tasks"] = []

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # 🧠 App layout begins here
    # st.set_page_config(page_title="ADHD Scheduler", layout="wide")
    st.title("🧠 Personal Time Manager")

    # 🧾 Task Form
    with st.form("task_form"):
        st.subheader("📥 Add a Task")
        title = st.text_input("Task Name")
        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time")

        fixed = st.checkbox("Is this a fixed event?")
        priority = st.selectbox("Priority", ["ASAP", "Urgent", "Normal", "Flexible"])
        submitted = st.form_submit_button("Add Task")

        dt_start = datetime.combine(datetime.today(), start_time)
        dt_end = datetime.combine(datetime.today(), end_time)
        duration = int((dt_end - dt_start).total_seconds() // 60)

        if submitted:
            if duration <= 0:
                st.warning("⚠️ End time must be after start time.")
            else:
                task = {
                    "title": title,
                    "start_time": dt_start,
                    "end_time": dt_end,
                    "duration": duration,
                    "priority": priority,
                    "fixed": fixed,
                }
                st.session_state.tasks.append(task)
                st.success(f"✅ Added: {title} ({duration} min)")

    # 🧾 View & Delete Tasks
    if st.session_state.tasks:
        st.subheader("📋 Tasks")

        for i, t in enumerate(st.session_state.tasks):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(
                    f"🔹 **{t['title']}** | {t['duration']} min | "
                    f"Fixed: {t['fixed']} | Priority: {t['priority']} | "
                    f"Start: {t['start_time'].strftime('%H:%M')} → End: {t['end_time'].strftime('%H:%M')}"
                )
            with col2:
                if st.button("❌", key=f"delete_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

    # 📅 Generate Schedule
    if st.button("📅 Generate Schedule"):
        final_schedule = schedule_tasks(st.session_state.tasks)
        final_schedule.sort(key=lambda x: x["start_time"])

        st.subheader("🗓️ Final Schedule")
        for task in final_schedule:
            start = task["start_time"].strftime("%H:%M")
            end = task["end_time"].strftime("%H:%M")
            st.write(f"📌 {task['title']} → {start} to {end} | Priority: {task['priority']} | Fixed: {task['fixed']}")

    # 🌙 Reflection Section
    st.subheader("🌙 Daily Reflection")
    st.write("Log how long tasks actually took:")

    with st.form("reflection_form"):
        task_titles = [t["title"] for t in st.session_state.tasks]
        selected = st.selectbox("Task to reflect on", task_titles)
        actual_time = st.number_input("Actual time (minutes)", min_value=1, max_value=300)
        reflect_submit = st.form_submit_button("Submit Reflection")

        if reflect_submit:
            st.session_state.completed_tasks.append({
                "title": selected,
                "actual_duration": actual_time
            })

            planned = next(t["duration"] for t in st.session_state.tasks if t["title"] == selected)

            feedback = get_ai_feedback(selected, planned, actual_time)
            st.success("🧠 Feedback:")
            st.info(feedback)

    # 💬 Chat with AI
    st.subheader("💬 Clarity Compass")

    user_input = st.text_input("You:", key="chat_input")

    if st.button("Send"):
        if user_input:
            ai_reply = chat_with_ai(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Gemini", ai_reply))
            del st.session_state["chat_input"]
            st.rerun()
        else:
            st.warning("Please enter a message before sending.")

    # Show chat history (always visible)
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")
        for speaker, msg in st.session_state.chat_history:
            st.markdown(f"**{speaker}:** {msg}")
    
    # Back to Home Button
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()