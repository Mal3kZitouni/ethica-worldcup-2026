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
- Example response for betting-related questions: "P&A World Cup 2026 est un jeu  gratuit (100 % free). créé uniquement pour s'amuser entre collègues ! Il n'y a aucun pari d'argent ni de mise réelle ici. On joue exclusivement pour le plaisir de la compétition, pour la gloire et pour grimper dans le classement de l'entreprise ! 🏆"

---
CORE CAPABILITIES (Match Analysis):
- Provide structured breakdowns including: current team form (last 5 matches), tactical matchups, historical head-to-head records, key player injuries, offensive/defensive statistics, and motivational factors.
- Always conclude match analyses with a realistic, data-backed score suggestion (e.g., "Based on current data, a 2-1 victory for France seems highly probable because...").

---
OFFICIAL GAME RULES & POINT SYSTEM (P&A World Cup 2026):
If a user asks about the rules, points, or how to play, explicitly present these exact rules using clean Markdown formatting:

1. Standard Match Predictions:
   - Exact Score Predicted = 5 Points
   - Correct Outcome (Winner or Draw) but Wrong Score = 3 Points
   - Make a Prediction = 1 Point
   - Wrong Prediction = 0 Points

2. Tournament Winner Bonus (Dynamic Prediction):
   Points awarded depend strictly on the STAGE at which the user submits their choice for the final 'Winner of the Tournament':
   - Group Stage: 15 Points
   - Round of 32: 12 Points
   - Round of 16: 10 Points
   - Quarter-Finals: 7 Points
   - Semi-Finals: 5 Points
   - Final Stage: 3 Points

---
BEHAVIOR & TONE:
- Always reply in the exact language used by the user (French or English).
- Be polite, professional, and use football emojis (⚽, 🏆, 📊, 🎯).
"""

def render_chat_panel():
    """Affiche l'assistant IA de manière innovante pour la colonne de droite"""
    
    # 1. INJECTION DU CSS (Antigravité & Glassmorphism)
    st.markdown("""
        <style>
            /* Animation d'antigravité */
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
            /* Style pour l'en-tête du chat */
            .chat-header {
                text-align: center;
                padding: 15px;
                background: linear-gradient(145deg, rgba(141,64,218,0.1), rgba(230,190,234,0.1));
                border-radius: 20px;
                border: 1px solid rgba(141,64,218,0.2);
                margin-bottom: 20px;
            }
            .chat-title {
                color: #242424;
                font-weight: 800;
                margin-top: 10px;
                font-size: 1.2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # 2. EN-TÊTE ANIMÉ
    st.markdown("""
        <div class="chat-header">
            <div class="floating-bot">🤖</div>
            <div class="chat-title">Performance & Analytics AI</div>
            <div style="color: #666; font-size: 0.9rem;">Assistant Tactique en direct</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. INITIALISATION DE LA MÉMOIRE
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Bonjour ! Prêt à grimper dans le classement P&A ? Posez-moi vos questions. ⚽"}
        ]

    # 4. ZONE DE DISCUSSION
    chat_container = st.container(height=500, border=False) # Hauteur fixe pour scroller proprement
    
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # 5. INPUT DE L'UTILISATEUR ET APPEL API
    if user_input := st.chat_input("Demandez une analyse...", key="main_chat_input"):
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)

        with chat_container:
            with st.chat_message("assistant"):
                try:
                    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
                    
                    if not api_key:
                        st.error("🔑 Clé API manquante (GROQ_API_KEY).")
                        return
                    
                    client = Groq(api_key=api_key)
                    
                    api_messages = [{"role": "system", "content": AI_CONTEXT}] + \
                                   [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=api_messages,
                        stream=True, 
                    )
                    
                    def generate_chunks():
                        for chunk in response:
                            if chunk.choices[0].delta.content:
                                yield chunk.choices[0].delta.content
                    
                    full_response = st.write_stream(generate_chunks())
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")

    @st.dialog("🤖 Prophet AI")
    def open_ai_dialog():
        render_chat_panel()