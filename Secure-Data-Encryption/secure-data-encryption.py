import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# Generate encryption key (in production, store this securely)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# In-memory data store
stored_data = {}
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = True  # Default True unless 3 fails

# Hashing function for passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt user data
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Decrypt user data
def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)

    for key, value in stored_data.items():
        if key == encrypted_text and value["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()
    
    st.session_state.failed_attempts += 1
    return None

# UI Begins
st.set_page_config(page_title="🔐 Secure Data App", layout="centered")
st.title("🔐 Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

# Home
if choice == "Home":
    st.subheader("🏠 Welcome!")
    st.write("This app lets you securely **store and retrieve sensitive data** using encryption and passkeys.")

# Store Data
elif choice == "Store Data":
    st.subheader("📥 Store New Data")
    user_text = st.text_area("Enter the data to secure:")
    user_passkey = st.text_input("Enter a passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_text and user_passkey:
            hashed = hash_passkey(user_passkey)
            encrypted = encrypt_data(user_text)
            stored_data[encrypted] = {"encrypted_text": encrypted, "passkey": hashed}
            st.success("✅ Data encrypted and stored successfully!")
            st.code(encrypted, language="text")
        else:
            st.error("⚠️ Please fill in all fields.")

# Retrieve Data
elif choice == "Retrieve Data":
    if not st.session_state.is_logged_in:
        st.warning("🔒 Too many failed attempts. Please login.")
        st.stop()

    st.subheader("🔍 Retrieve Stored Data")
    encrypted_input = st.text_area("Paste the encrypted text:")
    passkey_input = st.text_input("Enter your passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_input and passkey_input:
            decrypted = decrypt_data(encrypted_input, passkey_input)
            if decrypted:
                st.success("✅ Success! Here's your decrypted data:")
                st.code(decrypted, language="text")
            else:
                attempts_left = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts remaining: {attempts_left}")
                if st.session_state.failed_attempts >= 3:
                    st.session_state.is_logged_in = False
                    st.warning("🔒 You have exceeded the maximum number of attempts.")
                    st.experimental_rerun()
        else:
            st.error("⚠️ Both fields are required.")

# Login Page
elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_password = st.text_input("Enter admin password to continue:", type="password")

    if st.button("Login"):
        if login_password == "admin123":  # For demo, replace with secure check in production
            st.session_state.failed_attempts = 0
            st.session_state.is_logged_in = True
            st.success("✅ Logged in successfully. You can now try again.")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect admin password.")
