import streamlit as st
import re
import random


st.set_page_config(page_title="Password Strength Meter", page_icon="🔐")



# List of common password
COMMON_PASSWORDS = ["password", "123456", "password123", "qwerty", "abc123", "iloveyou", "admin"]


# Auto Generate Password
def generate_password(length = 12):
    charc ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return "".join(random.choice(charc) for i in range(length))


# Check Passsword Strength
def check_password_strength(password):
    score = 0
    suggestions = []

    if password.lower() in COMMON_PASSWORDS:
        return "❌ This password is too common. Choose a stronger one!"
    
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

    return strength






# Page Title
st.title("🔐 Password Strength Meter")


st.write("")

length = st.slider("🔢 Choose password length (8-24 characters)", min_value=8, max_value=24, value=12)
password = st.text_input("Enter your password", placeholder="type your password", type="password", max_chars=length)


if password:
    strength = check_password_strength(password)
    st.subheader(strength)
