# app/langchain_rag.py
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI

def retrieve_and_generate(query):
    # Tải dữ liệu vào FAISS index để tìm kiếm
    vectorstore = FAISS.load_local("path_to_faiss_index")
    
    # Tạo một chuỗi truy vấn
    retriever = vectorstore.as_retriever()
    chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
    
    # Lấy kết quả từ mô hình RAG
    result = chain.run(query)
    
    return result
