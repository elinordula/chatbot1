import streamlit as st
st.title("Hello users")

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
credit_card_placeholder = st.empty()

with prompt_placeholder:
    cols = st.columns((6, 1))
    cols[0].text_inputs(
        "Chat",
        value = "Hello Bot"
    )
    
    cols[0].text_inputs(
        "Chat",
        value = "Hello Bot"
    )