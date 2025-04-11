# Imports 
import os
import streamlit as st
import fitz
from dotenv import load_dotenv
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain


# PDF Text Extraction
@st.cache_data
def load_stored_documents(pdf_folders = r"C:\Users\User\Documents\Projects\Mini_search_engine\books"):
    documents = []

    for filename in os.listdir(pdf_folders):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folders, filename)
            doc = fitz.open(pdf_path)

            full_text = ""
            for page in doc:
                full_text += page.get_text("text")

            if full_text.strip():
                documents.append(Document(
                    page_content=full_text,
                    metadata={"source": filename}
                ))
                print(f"Loaded: {filename}")
            else:
                print(f"Skipped (no text): {filename}")
    return documents

def process_uploaded_documents(uploaded_files):
    documents = []
    for file in uploaded_files:
        text=""
        file_name = file.name
        pdf = fitz.open(stream=file.read(), filetype="pdf")

        for page in pdf:
            text += page.get_text("text")
            metadata = {"source":file_name}

        if text.strip():
            documents.append(Document(page_content=text, metadata=metadata))
        
    return documents

# Chunking
def splitter_chunk_with_metadata(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    all_chunks = []
    for page in pages:
        docs = splitter.create_documents([page.page_content])
        for i , chunk in enumerate(docs):
            chunk.metadata = page.metadata.copy()
            chunk.metadata["chunk_id"]=i
            all_chunks.append(chunk)
    return all_chunks

# Prompt Templates
strict_prompt = PromptTemplate(
    input_variables =["context","question"],
    template="""
    You are a PDF assistant. Use ONLY the context below to answer the question.
    If the answer is not in the context, respond with: "The answer is not provided in the PDFs"

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
)
loose_prompt_template = """
    You are a helpful assistant. Use the context below to answer the question as best as you can.
    You can infer and reason using your own understanding, but do not make things up.
    
    Context:
    {context}
    
    Question: {question}
    Answer:"""

loose_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=loose_prompt_template
)


# Chain Constructors
def get_strict_chain(llm,retriever):
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model = 'gpt-4o-mini'),
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt":strict_prompt},
        return_source_documents=True
    )
def get_loose_chain(llm, retriever):
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",  
        return_source_documents=False,  
        chain_type_kwargs={"prompt":loose_prompt}
        )


# LLM Review Function 
def review_with_LLM(question, initial_answer, llm):
    review_prompt = f"""
You are a helpful AI assistant.

Here is a question and its original answer based only on some context.

Question: {question}
Answer: {initial_answer}

Does this answer directly address the question? If not, explain briefly and then rewrite the answer to be more helpful and complete, using your own understanding.
If it’s already good, just say: "The answer is good.".
"""
    return llm.invoke(review_prompt).content


def ask_question(strict_chain,loose_chain,mode,query):

    st.write(f"You are using **{mode}** mode.")
    if mode == "Strict":
        result = strict_chain.invoke({"query": query})
        main_result = result["result"]
        st.markdown("### STRICT MODE")
        st.markdown("Answer:")
        st.write(main_result)
        st.markdown("### Sources:")
        for doc in result["source_documents"]:
            st.write(f" - {doc.metadata.get('source', 'Unknown')}")

    elif mode == "Loose":
        result = loose_chain.invoke(query)
        st.markdown("### LOOSE MODE]")
        st.markdown("### Answer")
        st.write(result)

    elif mode == "Enhanced":
        response = strict_chain.invoke({"query":query})
        result = response["result"]
        llm=ChatOpenAI(model = 'gpt-4o-mini')
        reviewed = review_with_LLM(
            question=query,
            initial_answer=result,
            llm=llm)
        st.markdown("### ENHANCED MODE]")
        st.markdown("### LLM Review Output:")
        st.write(reviewed)
        st.markdown("### Sources:")
        for doc in response["source_documents"]:
            st.write(f" - {doc.metadata.get('source', 'Unknown')}")
        

    else:
        st.write("Invalid mode. Use 'strict' or 'loose'")


def main():
    load_dotenv()
    llm = ChatOpenAI(temperature=0)

    st.set_page_config(page_title="Mini Search Engine", layout="wide")

    st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
    }

    input[type="text"] {
        background-color: #1E1E1E;
        color: white;
    }

    textarea {
        background-color: #1E1E1E;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
    st.title("Mini Search Engine For Radiography PDFs and Any PDF of your choice....")

    stored_docs = load_stored_documents()

    uploaded_files = st.file_uploader("Upload multiple PDFs", type="pdf", accept_multiple_files=True)

    uploaded_docs = []
    if uploaded_files:
        with st.spinner("Processing uploaded PDFs..."):
            uploaded_docs = process_uploaded_documents(uploaded_files)
    all_docs = stored_docs + uploaded_docs

    if "query_input" not in st.session_state:
        st.session_state["query_input"] = ""
    if "mode_select" not in st.session_state:
        st.session_state["mode_select"] = "Strict"
    
    query = st.text_input("Ask your question here", key="query_input")
    mode = st.radio(
        "Select answer mode", 
        ["Strict", "Loose", "Enhanced"], 
        key="mode_select", 
        help="Choose how the AI answers: source_based, flexible, or LLM-reviewed"
    )

    col1, col2 = st.columns(2)
    with col1:
        submit = st.button("Submit", key="submit_button")
    with col2:
        clear = st.button("Clear", key="clear_button")
    
    if clear:
        st.session_state["query_input"]=""
        st.session_state["mode_select"]="Strict"
        st.rerun()
    
    if submit and query and all_docs:
        with st.spinner("Processing your request..."):
            chunks = splitter_chunk_with_metadata(all_docs)
            embeddings = OpenAIEmbeddings()
            vector_db = Chroma.from_documents(chunks, embeddings)
            retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k":6})

            loose_chain = get_loose_chain(llm, retriever)
            strict_chain = get_strict_chain(llm, retriever)

            ask_question(strict_chain,loose_chain,mode,query)

   





if __name__ == "__main__":
    main()

