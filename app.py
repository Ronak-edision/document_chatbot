import streamlit as st
from langchain import read_file, query_cohere

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
        if st.session_state.rag_chain:
            try:
                prompt = f"Here are some documents: {st.session_state.rag_chain}\n\nQ: {query}\nA:"
                answer = query_cohere(prompt)
                st.write(f"Answer: {answer}")

                # Check if the user asked for a call
                if "call" in query.lower():
                    st.session_state.call_request = True
                    st.write("It looks like you want us to call you. Please provide your contact details below.")
                else:
                    st.session_state.call_request = False
            except Exception as e:
                st.write(f"An error occurred: {e}")
        else:
            st.error("Please process the documents first.")
    else:
        st.error("Please enter a question.")

# Contact Form Section
if st.session_state.call_request:
    with st.sidebar.form(key='contact_form'):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        submit_button = st.form_submit_button("Submit Contact Info")

        if submit_button:
            if name and phone and email:
                st.sidebar.write(f"Name: {name}")
                st.sidebar.write(f"Phone: {phone}")
                st.sidebar.write(f"Email: {email}")
                st.sidebar.write("Your information has been submitted. We'll get in touch with you soon.")
                st.session_state.call_request = False  # Reset call request after submission
            else:
                st.sidebar.error("Please fill in all the fields.")
else:
    # Display greeting and explanation if no call request
    st.sidebar.title("Welcome!")
    st.sidebar.write(
        "Welcome to the Document Q&A Chatbot. Ask me anything about the documents you uploaded, and I'll provide you with the insights.")
    st.sidebar.write(
        "If you need a call back, simply ask for it, and I will prompt you to provide your contact information.")
