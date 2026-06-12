import streamlit as st
from groq import Groq
import os

AI_CONTEXT = """
You are Prophet AI, an advanced sports analytics assistant developed exclusively for the P&A World Cup 2026 prediction application.

🛑 CRITICAL SECURITY RULE (STRICT SCOPE CONSTRAINT):
You are strictly programmed to ONLY answer questions regarding the P&A World Cup 2026 prediction game, football match analysis, team statistics, and the official point system rules.
- If a user asks about ANY other topic (including but not limited to: coding, recipes, general knowledge, math, history, other sports), you MUST politely but firmly refuse to answer.

⚠️ STRICT NO-BETTING / NO-GAMBLING POLICY (FRIENDLY CORPORATE GAME):
This application is purely a friendly, free corporate game designed for fun, team building, and entertainment among colleagues. It is absolutely NOT a betting, gambling, or real-money wagering platform.

- If a user mentions money, bets, financial odds, gambling, or asks how to withdraw/deposit funds, you MUST explicitly clarify that this is a 100% free game for fun with colleagues, with no real money involved.

CORE CAPABILITIES:
- Analyze football matches.
- Explain tournament rules.
- Explain scoring system.
- Discuss rankings.
- Provide team and tournament insights.

BEHAVIOR:
- Always answer in the language used by the user.
- Use football emojis when appropriate.
"""

def render_chat_panel():

    st.markdown("""
    <style>

    @keyframes antigravity {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
        100% { transform: translateY(0px); }
    }

    .floating-bot {
        animation: antigravity 4s ease-in-out infinite;
        display: inline-block;
        font-size: 3.5rem;
        text-shadow: 0 10px 15px rgba(141, 64, 218, 0.4);
    }

    .chat-header {
        text-align: center;
        padding: 18px;
        background: linear-gradient(
            135deg,
            rgba(141,64,218,0.12),
            rgba(73,38,79,0.08)
        );
        border-radius: 22px;
        border: 1px solid rgba(141,64,218,0.25);
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(141,64,218,0.08);
    }

    </style>
    """, unsafe_allow_html=True)

    # ==================================================
    # HEADER
    # ==================================================

    st.markdown(
        """
        <div class="chat-header">
            <div class="floating-bot">🤖</div>
            <p style="color:#666;font-size:0.95rem;font-weight:600;margin-top:10px;">
                ⚽ World Cup Predictions • 📊 Match Insights • 🏆 Ranking Assistant
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # MEMORY
    # ==================================================
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content":
                "👋 Welcome! Ask me anything about the World Cup 2026, match predictions, rankings, or tournament rules."
            }
        ]

    # ==================================================
    # CHAT HISTORY
    # ==================================================
    chat_container = st.container(
        height=320,
        border=False
    )

    with chat_container:

        for msg in st.session_state.messages:

            with st.chat_message(msg["role"]):

                st.markdown(msg["content"])

    # ==================================================
    # INPUT
    # ==================================================
    if user_input := st.chat_input(
        "Ask for a match analysis...",
        key="main_chat_input"
    ):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with chat_container:

            with st.chat_message("user"):

                st.markdown(user_input)

        with chat_container:

            with st.chat_message("assistant"):

                try:

                    api_key = (
                        os.environ.get("GROQ_API_KEY")
                        or
                        st.secrets.get("GROQ_API_KEY")
                    )

                    if not api_key:

                        st.error(
                            "🔑 API key missing (GROQ_API_KEY)."
                        )

                        return

                    client = Groq(api_key=api_key)

                    api_messages = [
                        {
                            "role": "system",
                            "content": AI_CONTEXT
                        }
                    ] + [
                        {
                            "role": m["role"],
                            "content": m["content"]
                        }
                        for m in st.session_state.messages
                    ]

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=api_messages,
                        stream=True,
                    )

                    def generate_chunks():

                        for chunk in response:

                            if chunk.choices[0].delta.content:

                                yield chunk.choices[0].delta.content

                    full_response = st.write_stream(
                        generate_chunks()
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": full_response
                        }
                    )

                except Exception as e:

                    st.error(
                        f"❌ Error: {str(e)}"
                    )


@st.dialog("⚽ Prophet AI")
def open_ai_dialog():

    render_chat_panel()