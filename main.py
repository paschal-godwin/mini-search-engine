# === Imports ===
# Put all import statements here
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
def extract_text_with_metadata(pdf_folders):
    documents = []
    for filename in os.listdir(pdf_folders):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folders, filename)
            doc = fitz.open(pdf_path)

            full_text = ""
            for page in doc:
                full_text += page.get_text()

            if full_text.strip():
                documents.append(Document(
                    page_content=full_text,
                    metadata={"source": filename}
                ))
                print(f"Loaded: {filename}")
            else:
                print(f"Skipped (no text): {filename}")
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
def review_answer_with_llm(question, initial_answer, llm):
    review_prompt = f"""
You are a helpful AI assistant.

Here is a question and its original answer based only on some context.

Question: {question}
Answer: {initial_answer}

Does this answer directly address the question? If not, explain briefly and then rewrite the answer to be more helpful and complete, using your own understanding.
If it’s already good, just say: "The answer is good.".
"""
    return llm.invoke(review_prompt).content

# Setup / Config
load_dotenv()
pdf_folders = r"C:\Users\User\Documents\Projects\Mini_search_engine\books"
pages = extract_text_with_metadata(pdf_folders)
chunks = splitter_chunk_with_metadata(pages)
embedding = OpenAIEmbeddings()

vector_db = Chroma.from_documents(chunks, embedding)
retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k":6})
llm = ChatOpenAI(temperature=0)
strict_chain = get_strict_chain(llm, retriever)
loose_chain = get_loose_chain(llm, retriever)

# Ask Question Function
def ask_question(mode, query):
    if mode == "strict":
        result = strict_chain.invoke({"query": query})
        print("\n[STRICT MODE]")
        print("Answer:", result["result"])
        print("Sources:")
        for doc in result["source_documents"]:
            print(f" - {doc.metadata.get('source', 'Unknown')}")

    elif mode == "loose":
        result = loose_chain.invoke(query)
        print("\n[LOOSE MODE]")
        print("Answer:", result)

    elif mode == "enhanced":
        response = strict_chain.invoke({"query":query})
        result = response["result"]
        llm=ChatOpenAI(model = 'gpt-4o-mini')
        reviewed = review_answer_with_llm(
            question=query,
            initial_answer=result,
            llm=llm)
        print("\n[ENHANCED MODE]")
        print("\nLLM Review Output:\n", reviewed)
        print("\nSources:")
        for doc in response["source_documents"]:
            print(f" - {doc.metadata.get('source', 'Unknown')}")
        

    else:
        print("Invalid mode. Use 'strict' or 'loose'")

# Example Call
ask_question("enhanced", "Who is the father of radiography?")
