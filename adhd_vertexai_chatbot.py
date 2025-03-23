import streamlit as st
import google.generativeai as genai
import os

def virtual_consultation():
    # Configure the Gemini API key
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Initial instructions for the chatbot
    initial_instruction = """
    You're a friendly ADHD coach who helps students manage tasks, stay focused, and feel supported.
    Be a personal companion to the user. 

    User background:
    - The user likely has ADHD (inattentive, hyperactive, or combined type), which may affect their focus, energy, time management, motivation, and emotional regulation.
    - They may struggle with task initiation, procrastination, or remembering instructions.
    - They could be a student or young adult juggling school, responsibilities, and personal goals.
    - They may have been misunderstood in traditional learning environments and are looking for compassionate, neurodivergent-friendly support.
    - They often know what they *want* to do, but struggle to get started or stay consistent.
    - They may deal with shame, anxiety, or burnout from trying to keep up with neurotypical systems.
    - They appreciate encouragement, structure, and practical advice that doesn't feel overwhelming.
    - They may already use tools like timers, planners, ADHD meds, or body-doubling—but need help making these stick.

    Your role:
    - Provide clear, actionable, and ADHD-friendly guidance
    - Offer both study-related and non-study task help
    - Use creative, non-traditional ADHD strategies if helpful

    Always respond with:
    - A kind, optimistic, and non-judgmental tone
    - Short paragraphs with helpful formatting
    - A **complete step-by-step breakdown** when asked for routines, plans, or "how to start"
    - Encouraging words and a **specific next action** the user can take

    Important:
    - If the user asks for help, **give the full method or process up front**
    - Avoid repeatedly asking the user for more input unless clarification is needed
    - If the user is stuck, anxious, or overwhelmed, offer grounding words and simple next steps

    You're patient, warm, and motivating. Help the user feel like progress is possible right now.
    """

    # Start the chat session with initial instructions
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[{"role": "user", "parts": [initial_instruction]}])

    # Streamlit app layout
    st.title("🧠 Virtual Buddy")
    st.write("Hey! I'm your Virtual buddy. Whether it's to do with studies or other parts of life, what can I help you with today? (Type 'quit' to exit)")

    # Display chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("You: ")

    if user_input:
        if user_input.lower() in ["quit", "exit"]:
            st.session_state.messages.append({"role": "assistant", "content": "Great work today! Take a break or keep up the momentum 💪"})
            st.rerun()
        else:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Send user input to the chatbot
            try:
                response = st.session_state.chat.send_message(user_input)
                assistant_response = response.text

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            except Exception as e:
                st.error(f"Error: {e}")

        # Rerun to update the chat display
        st.rerun()

    # Back to Home Button
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# # Run the virtual consultation
# virtual_consultation()