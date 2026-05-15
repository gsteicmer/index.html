import streamlit as st
import requests

# Page visual configuration
st.set_page_config(page_title="FounderLogic AI", page_icon="🚀", layout="centered")
st.title("🚀 FounderLogic AI")
st.subheader("Startup Viability Analysis in Real Time")

# User input fields
idea_name = st.text_input("What is the name of your idea?", placeholder="Ex: SafeChain Protocol")
description = st.text_area("Describe the problem and the solution:", placeholder="Explain how your idea works...")

if st.button("Generate Verdict"):
    if idea_name and description:
        with st.spinner("The Agent is searching Google and analyzing..."):
            # PASTE YOUR N8N WEBHOOK URL (PRODUCTION) HERE
            webhook_url = "https://flow-automation-studio.app.n8n.cloud/webhook/c04361c7-bfd9-4e8e-9173-fcd8c905e05f"

            payload = {
                "Name of Your Idea": idea_name,
                "Describe the problem and its solution": description
            }

            try:
                response = requests.post(webhook_url, json=payload, timeout=60)  # ✅ timeout adicionado aqui

                if response.status_code == 200:
                    # Receiving structured data from Respond to Webhook
                    data = response.json()

                    st.divider()

                    # Displaying Score and Verdict in a beautiful way
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Market Score", f"{data['score']}/10")
                    with col2:
                        color = "green" if data['verdict'] == "VALIDATE" else "red"
                        st.markdown(f"### Verdict: :{color}[{data['verdict']}]")

                    st.markdown("#### 📝 Detailed Analysis")
                    st.write(data['analysis'])

                else:
                    st.error(f"Server error: {response.status_code}")

            except Exception as e:
                st.error(f"Could not connect to n8n: {e}")
    else:
        st.warning("Please fill in both the idea name and description.")