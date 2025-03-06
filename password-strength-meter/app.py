import streamlit as st
import re
import random
from io import BytesIO
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Password Strength Meter", page_icon="🔐")



# List of common password
common_password = ["password", "123456", "password123", "qwerty", "abc123", "iloveyou", "admin"]





# Auto Generate Password
def generate_password(length = 12):
    charc ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return "".join(random.choice(charc) for i in range(length))


# Check Passsword Strength
def check_password_strength(password):
    score = 0
    suggestions = []

    if password.lower() in common_password:
        return "❌ This password is too common. Choose a stronger one!", []
    
    # Scoring
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("🔹 Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 2
    else:
        suggestions.append("🔹 Add at least one uppercase letter (A-Z).")

    if re.search(r"[a-z]", password):
        score += 2
    else:
         suggestions.append("🔹 Add at least one lowercase letter (a-z).")

    if re.search(r"\d", password):
        score += 2  # Numbers are important, so higher weight
    else:
        suggestions.append("🔹 Include at least one digit (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 2  # Special characters have the highest weight
    else:
        suggestions.append("🔹 Use at least one special character (!@#$%^&*).")

# Scoring
    if score <= 3:
        strength = "Weak 🔴"
    elif score <= 7:
        strength = "Moderate 🟡"
    else:
        strength = "Strong 🟢"

    return strength, suggestions






# Page Title
st.title("🔐 Password Strength Meter")
# for line space
st.write("")


password = st.text_input("Enter your password", placeholder="type your password", type="password")

# passwword instructions
if password:
    strength, feedback = check_password_strength(password)
    st.subheader(strength)

    if feedback:
        st.warning("🔽 Suggestions to improve:")
        for suggestion in feedback:
            st.write(suggestion)
    else:
        st.success("✅ Your password is strong!")


# 🎲 Generate a Strong Password
st.subheader("Auto Generate Password")
length = st.slider("🔢 Choose password length (8-24 characters)", min_value=8, max_value=24, value=12)

if st.button("Generate Strong Password"):
    strong_password = generate_password(length)
    st.session_state.password_history.append(strong_password)
    genrated_pass = st.text(f"Suggested Password: {strong_password}")



# 👉 Function to Create and Download PDF
def create_pdf(passwords):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Password History")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 800, "🔐 Password History")

    pdf.setFont("Helvetica", 12)
    y = 780
    for i, pwd in enumerate(reversed(passwords), 1):  # Show latest first
        pdf.drawString(100, y, f"{i}. {pwd}")
        y -= 20  # Move down

    pdf.save()
    buffer.seek(0)
    return buffer
# Side-Bar
with st.sidebar:

    st.header("your password history")

    if "password_history" not in st.session_state:
        st.session_state.password_history = [] 

    if password:
        st.session_state.password_history.append(password)  # Add new password
    
# 👉 Show password history
    for i in reversed(st.session_state.password_history):  # Show latest first
        st.write(f"🔹 {i}")

    # Clear history button
   
    if st.button("🗑️ Clear History"):
        st.session_state.password_history = []
        st.rerun()

    # Download password history
    if st.session_state.password_history:
        pdf_buffer = create_pdf(st.session_state.password_history)
        st.download_button(label="📥 Download Password History (PDF)", 
                           data=pdf_buffer, 
                           file_name="password_history.pdf", 
                           mime="application/pdf")