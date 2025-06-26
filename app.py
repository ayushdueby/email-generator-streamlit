import streamlit as st
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import csv

# === Gmail API Email Sending Function ===
def send_email_via_gmail(subject, body, recipient):
    try:
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.send'])
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(body)
        message['to'] = recipient
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message = {'raw': raw}

        sent_message = service.users().messages().send(userId="me", body=message).execute()
        return f"Email sent successfully to {recipient}! ID: {sent_message['id']}"
    except Exception as e:
        return f"Failed to send email to {recipient}: {str(e)}"

# === Read Emails from CSV ===
def read_recipients_from_csv(filename):
    recipients = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'email' in row and row['email'].strip():
                recipients.append(row['email'].strip())
    return recipients

# === Read content from file ===
def read_content_from_file(filename):
    with open(filename, "r") as file:
        return file.read()

# === Convert image to base64 ===
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# === Streamlit UI ===
st.set_page_config(
    page_title="Generate & Send Emails",
    page_icon='📧',
    layout='centered',
    initial_sidebar_state='collapsed'
)

# Set your image path
image_path = "Screenshot (907).png"
base64_bg = get_base64_image(image_path)

# === Background Image Styling ===
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/png;base64,{base64_bg}');
        background-size: cover;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Generate & Send Emails 📧")

# Load default content from file
form_content_file = r"C:\Users\ayush\OneDrive\Desktop\langchaain projects\Email Generator App - Source Code\mail text"
default_text = read_content_from_file(form_content_file)

# Prefill the text area with editable content
form_input = st.text_area('Enter the email topic or message', value=default_text, height=275)

col1, col2 = st.columns(2)
with col1:
    email_sender = st.text_input('Sender Name')
    email_subject = st.text_input('Email Subject')
with col2:
    email_csv_file = r"C:/Users/ayush/OneDrive/Desktop/langchaain projects/Email Generator App - Source Code/emails.csv"
    email_recipients = read_recipients_from_csv(email_csv_file)
    email_style = st.selectbox(
        'Writing Style',
        ('Formal', 'Appreciating', 'Not Satisfied', 'Neutral'),
        index=0
    )

# Initialize session state if not already
if "email_body" not in st.session_state:
    st.session_state.email_body = ""
if "email_ready" not in st.session_state:
    st.session_state.email_ready = False

if st.button("Generate Email"):
    st.session_state.email_body = form_input
    st.session_state.email_ready = True
    st.success("Email Generated ✅")

if st.session_state.email_ready:
    st.markdown("**Preview:**")
    st.write(st.session_state.email_body)

    if st.button("Send Email via Gmail"):
        with st.spinner("Sending Email..."):
            results = [send_email_via_gmail(email_subject, st.session_state.email_body, recipient) for recipient in email_recipients]
            for res in results:
                st.success(res)
            st.session_state.email_ready = False  # Reset after sending
