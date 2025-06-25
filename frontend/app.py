import streamlit as st

# Set page title and icon
st.set_page_config(page_title="NLPcraft", page_icon="🤖")

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "login"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Dummy users (use database in production)
users = {
    "admin": {"password": "admin123", "email": "admin@example.com"},
}

# -------------------- Pages --------------------

def login_page():
    st.title("NLPcraft 🤖")
    st.subheader("Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = users.get(username)
        if user and user["password"] == password:
            st.session_state.authenticated = True
            st.session_state.page = "home"
        else:
            st.error("Invalid credentials")

    if st.button("Go to Sign Up"):
        st.session_state.page = "register"


def register_page():
    st.title("NLPcraft 🤖")
    st.subheader("Sign Up")

    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Sign Up"):
        if username in users:
            st.warning("Username already exists!")
        else:
            users[username] = {"password": password, "email": email}
            st.success("User registered. You can log in now.")
            st.session_state.page = "login"

    if st.button("Back to Login"):
        st.session_state.page = "login"


def home_page():
    st.title("Welcome to NLPcraft 🤖")
    st.sidebar.title("Apps")
    
    app = st.sidebar.radio("Select Application", ["Sentiment", "NER", "QA"])

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.page = "login"

    if app == "Sentiment":
        sentiment_page()
    elif app == "NER":
        ner_page()
    elif app == "QA":
        qa_page()


# -------------------- Tools --------------------

def sentiment_page():
    st.subheader("Sentiment Analysis")
    text = st.text_area("Enter your text:")
    if st.button("Analyze"):
        st.info(f"Sentiment result for: {text} (dummy result here)")


def ner_page():
    st.subheader("Named Entity Recognition")
    text = st.text_area("Enter your sentence:")
    if st.button("Extract Entities"):
        st.info(f"NER result for: {text} (dummy result here)")


def qa_page():
    st.subheader("Question Answering")
    context = st.text_area("Context:")
    question = st.text_input("Question:")
    if st.button("Get Answer"):
        st.info(f"Answer to: {question} (dummy result here)")


# -------------------- Main Navigation --------------------

if not st.session_state.authenticated:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()
else:
    home_page()
