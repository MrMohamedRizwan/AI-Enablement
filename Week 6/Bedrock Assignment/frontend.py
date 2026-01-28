import streamlit as st
import boto3
from datetime import datetime

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Bedrock Web Scraper Agent",
    page_icon="🕸️",
    layout="wide"
)

# ----------------------------
# Header
# ----------------------------
st.markdown("""
<style>
.chat-container {
    max-width: 900px;
    margin: auto;
}
.user-msg {
    background-color: #DCF8C6;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}
.agent-msg {
    background-color: #F1F0F0;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: left;
}
.footer-input {
    position: sticky;
    bottom: 0;
    background: white;
    padding-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🕸️ Web Scraper Agent")
st.caption("Amazon Bedrock Agent • Crawl • Clean • Summarize")

# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

# ----------------------------
# Agent Configuration (Expander)
# ----------------------------
with st.expander("⚙️ Agent Configuration", expanded=False):
    aws_region = st.text_input("AWS Region", "us-east-1")
    agent_id = st.text_input("Agent ID")
    agent_alias_id = st.text_input("Agent Alias ID", "TSTALIASID")

# ----------------------------
# Bedrock Invoke Function
# ----------------------------
def invoke_agent(prompt):
    client = boto3.client(
        "bedrock-agent-runtime",
        region_name=aws_region
    )

    response = client.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=st.session_state.session_id,
        inputText=prompt
    )

    final_text = ""
    for event in response["completion"]:
        if "chunk" in event:
            final_text += event["chunk"]["bytes"].decode("utf-8")

    return final_text

# ----------------------------
# Chat Area
# ----------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="agent-msg">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Input Bar (Bottom)
# ----------------------------
st.markdown('<div class="footer-input">', unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])

with col1:
    user_prompt = st.text_input(
        "Ask the agent to scrape a website…",
        placeholder="Scrape https://example.com and summarize",
        label_visibility="collapsed"
    )

with col2:
    send = st.button("Send 🚀", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Handle Send
# ----------------------------
if send and user_prompt:
    if not agent_id:
        st.error("Agent ID is required")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": user_prompt
        })

        with st.spinner("Agent is thinking..."):
            try:
                response = invoke_agent(user_prompt)
                st.session_state.messages.append({
                    "role": "agent",
                    "content": response
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "agent",
                    "content": f"❌ Error: {str(e)}"
                })

        st.rerun()

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption(f"Session ID: `{st.session_state.session_id}`")
