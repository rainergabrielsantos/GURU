import os
import streamlit as st
from utils import apply_custom_theme
from utils import apply_custom_theme
from google import genai
from dotenv import load_dotenv
# --- GOOGLE GENAI (GEMINI) ---
try:
    # new google-genai SDK
    from google import genai
except ImportError:
    genai = None

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Chat with GURU",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_theme()

# ---------- LOAD API KEY FROM .env ----------
load_dotenv()  # this reads .env in your project root
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found. Make sure it's set in your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# Validate API + SDK
if genai is None:
    st.error(
        "❌ google-genai is not installed.\n\n"
        "Run:\n\n"
        "```bash\npip install google-genai\n```"
    )
    st.stop()

if not api_key:
    st.error(
        "❌ GOOGLE_API_KEY not found.\n\n"
        "Do one of the following:\n"
        "1. Add `GOOGLE_API_KEY` \n"
        "2. Create a `.env` file with:\n"
        "   GOOGLE_API_KEY=YOUR_KEY_HERE"
    )
    st.stop()

# Create the Gemini client
client = genai.Client(api_key=api_key)

# ---------- UI HEADER ----------
left_col, right_col = st.columns([3, 2])

with left_col:
    st.title("GURU Chatbot")
    st.caption(
        "Your AI business advisor for this soda storefront. Ask about sales trends, "
        "inventory risk, restocking, or pricing ideas."
    )

with right_col:
    st.markdown(
        """
        <div style="
            margin-top: 0.8rem;
            padding: 0.9rem 1rem;
            border-radius: 14px;
            background: rgba(15,23,42,0.95);
            border: 1px solid rgba(148,163,184,0.35);
            font-size: 0.8rem;
        ">
            <div style="font-weight:600; margin-bottom:0.2rem;">Sample questions for GURU:</div>
            <ul style="padding-left: 1.1rem; margin: 0.2rem 0 0;">
                <li>"Which soda SKUs are most at risk of going out of stock this week?"</li>
                <li>"Summarize today's sales in 3 quick bullet points."</li>
                <li>"Suggest a weekend promo using our top-selling flavors."</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------- CHAT STATE ----------
if "guru_messages" not in st.session_state:
    st.session_state.guru_messages = [
        {
            "role": "assistant",
            "content": (
                "Hi, I'm **GURU** 🧠🥤 — your AI business advisor for this soda business.\n\n"
                "Ask me about inventory, sales performance, pricing strategies, or promotions, "
                "and I'll give you practical, data-minded suggestions."
            ),
        }
    ]

# ---------- DISPLAY HISTORY ----------
for msg in st.session_state.guru_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- INPUT ----------
user_input = st.chat_input("Ask GURU anything about your business...")

if user_input:
    # Add user message
    st.session_state.guru_messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build conversation as plain text for the model
    convo_text = ""
    for m in st.session_state.guru_messages:
        speaker = "User" if m["role"] == "user" else "GURU"
        convo_text += f"{speaker}: {m['content']}\n\n"

    system_prompt = (
        "You are GURU, an AI business advisor focused on an online + retail soda business. "
        "You give concise, actionable advice using short paragraphs and bullet points. "
        "Prioritize insights about inventory risk, restocking, sales trends, pricing, and promotions. "
        "If you need more context, ask a brief, specific follow-up question."
    )

    full_prompt = system_prompt + "\n\nConversation so far:\n" + convo_text

    # ---------- CALL GEMINI ----------
    with st.chat_message("assistant"):
        with st.spinner("GURU is thinking..."):
            try:
                resp = client.models.generate_content(
                    model="gemini-2.5-flash",   # you can change to a different Gemini model if desired
                    contents=full_prompt,
                )
                reply = resp.text
            except Exception as e:
                reply = (
                    "I ran into an error talking to the Gemini API:\n\n"
                    f"`{e}`\n\n"
                    "Double-check your API key and billing/project settings in Google AI Studio."
                )

            st.markdown(reply)
            st.session_state.guru_messages.append(
                {"role": "assistant", "content": reply}
            )
