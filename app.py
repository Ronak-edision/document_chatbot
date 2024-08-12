import streamlit as st
from model import read_file, query_cohere

# Set Streamlit page configuration
st.set_page_config(page_title="Document Q&A Chatbot", layout="wide")

# File Upload and Processing
st.sidebar.title("Upload documents")
uploaded_files = st.sidebar.file_uploader("Drag and drop files here", type=["pdf", "xlsx", "csv", "txt"],
                                          accept_multiple_files=True)
process_button = st.sidebar.button("Process")

if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'call_request' not in st.session_state:
    st.session_state.call_request = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}  # Initialize user info dictionary

documents = []
if process_button:
    if uploaded_files:
        st.write("Processing documents...")
        for file in uploaded_files:
            documents.append(read_file(file))
        combined_docs = "\n\n".join(documents)
        st.session_state.rag_chain = combined_docs
        st.write("Documents processed successfully!")
    else:
        st.sidebar.error("Please upload at least one file.")

# Query Handling
st.title("Generate Insights")
query = st.text_input("Ask a question about your documents:")
if st.button("Submit"):
    if query:
        # Check for "call me" request first, regardless of document processing
        if "call" in query.lower():
            st.session_state.call_request = True
            if st.session_state.user_info:
                st.write(f"It looks like you want us to call you again, {st.session_state.user_info['name']}. We'll reach out to you soon!")
            else:
                st.write("It looks like you want us to call you. Please provide your contact details below.")

        # Only process document-related queries if documents have been processed
        if st.session_state.rag_chain:
            try:
                prompt = f"Here are some documents: {st.session_state.rag_chain}\n\nQ: {query}\nA:"
                answer = query_cohere(prompt)
                st.write(f"Answer: {answer}")
            except Exception as e:
                st.write(f"An error occurred: {e}")
        elif "call" not in query.lower():
            st.error("Please process the documents first to ask questions about them.")
    else:
        st.error("Please enter a question.")

# Contact Form Section
if st.session_state.call_request and not st.session_state.user_info:
    with st.sidebar.form(key='contact_form'):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        submit_button = st.form_submit_button("Submit Contact Info")

        if submit_button:
            if name and phone and email:
                # Store user information in session state
                st.session_state.user_info = {
                    "name": name,
                    "phone": phone,
                    "email": email
                }
                st.sidebar.write("Your information has been submitted. We'll get in touch with you soon.")
                st.session_state.call_request = False  # Reset call request after submission
            else:
                st.sidebar.error("Please fill in all the fields.")
else:
    # Display greeting and explanation if no call request or if user info already exists
    st.sidebar.title("Welcome!")
    st.sidebar.write(
        "Welcome to the Document Q&A Chatbot. Ask me anything about the documents you uploaded, and I'll provide you with the insights.")
    if st.session_state.user_info:
        st.sidebar.write(f"Hello again, {st.session_state.user_info['name']}!")
    st.sidebar.write(
        "If you need a call back, simply ask for it, and I will prompt you to provide your contact information.")
