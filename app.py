import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Display chat history in a single location (below the input box)
    st.markdown("<h3 style='text-align: center;'>Chat History</h3>", unsafe_allow_html=True)
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:  # User message
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:  # Bot response
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon="📚", layout="wide")
    st.write(css, unsafe_allow_html=True)

    # Header Section
    st.markdown(
        """
        <div style="background-color: #6c757d; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
            <h1 style="color: white; text-align: center;">Chat with Multiple PDFs 📚</h1>
            <p style="color: white; text-align: center; font-size: 16px;">Upload your documents and interact with them intelligently.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # User Interaction Section
    st.text_input(
        "Ask a question about your documents:",
        placeholder="Type your question here...",
        on_change=lambda: handle_userinput(st.session_state.user_question),
        key="user_question",
    )

    # Sidebar Section
    with st.sidebar:
        st.markdown(
            """
            <div style="background-color: #2a9d8f; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
                <h3 style="color: white; text-align: center;">📁 Your Documents</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)

                text_chunks = get_text_chunks(raw_text)

                vectorstore = get_vectorstore(text_chunks)

                st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == '__main__':
    main()
