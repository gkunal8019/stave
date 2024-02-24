from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

import os
import openai

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"


def blog(query):
    prompt=f"go through all the doccument give the corrected answer : {query}"
    openai = ChatOpenAI(model_name="gpt-4",temperature=0.7,max_tokens=4000) # 'ada' 'gpt-3.5-turbo' 'gpt-4'
    embeddings = OpenAIEmbeddings()
    new_db = FAISS.load_local("faiss_index_new-20240224T101307Z-001", embeddings)
    chain = load_qa_chain(openai, chain_type="stuff")
    docs = new_db.similarity_search(query,10)
    response=chain.run(input_documents=docs, question=prompt)
    return response

import gradio as gr
text_input = gr.Textbox(label="Type your question here")
output_text = gr.Textbox(label="AI-generated response")

title_html = "<h2 style='text-align:center;font-weight:bold;color:black;'> Magnawave </h2>"
desc_html = "<p style='text-align:center;'>Get instant responses to any question related to Magnawave by asking our AI chatbot.</p>"

chatbot_interface = gr.Interface(
    fn=blog,
    inputs=text_input,
    outputs=output_text,
    title=title_html,
    description=desc_html
)
chatbot_interface.launch(share=True)