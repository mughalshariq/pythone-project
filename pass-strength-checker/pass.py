import streamlit as st
import requests
import re

st.set_page_config(page_title="Password Generator", page_icon="🔒")
st.title("🔐Password Generator")
st.markdown( """
## welcome to the ultimate password strenght checker!
 use this tool to check the strength of your password and get suggestions on how to make it stronger
            we will give you help tips to create a **strong Password** """)

password = st.text_input("Enter your password", type="password")


feefback = []

score = 0

if password:
    if len(password) >= 8:
        score += 1
    else:
        feefback.append("❌Password should be at least 8 characters long")    
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
            score += 1
    else:
        feefback.append("❌Password should contain both uppercase and lowercase letters")
    if re.search(r'\d', password):
        score += 1    
    else:
        feefback.append("❌Password should contain at least one digit")
    if re.search(r'[@$!%*?&]', password):
        score += 1
    else:
        feefback.append("❌Password should contain at least one special character (@$!%*?&)")
    if score == 4:
        st.success("✅Your password is strong!🎉")
    elif score == 3:
         feefback.append("⚠️Your password is medium strength. it could be Strong.")
    else:
        feefback.append("❌Your password is weak. please make it Stronger.")
        if feefback:
         st.markdown("### Improvement Suggestions")
         for tip in feefback:
             st.write(tip)
        else:
         st.info("Please enter a password to get started.")         