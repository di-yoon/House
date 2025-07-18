#%%
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_pinecone import Pinecone
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
import os
from myexample import fewshot_examples
from dotenv import load_dotenv
load_dotenv()

os.makedirs('sqlite_cache', exist_ok=True)
set_llm_cache(SQLiteCache(database_path = './sqlite_cache/sqlite_cache.db'))

def load_vector_store():
    embeddings = OpenAIEmbeddings(model = 'text-embedding-3-large')
    vector_store = Chroma(
        persist_directory='./house',
        embedding_function=embeddings,
        collection_name='house'
    )
    return vector_store

def create_chain(vector_store):
    llm = ChatOpenAI(model = 'gpt-4.1', streaming = True)
    output_parser = StrOutputParser()
    retriever = vector_store.as_retriever()
    
    tuple_fewshow_examples = []
    for example in fewshot_examples:
        tuple_fewshow_examples.append(('human', example['question']))
        tuple_fewshow_examples.append(('ai', example['answer']))


    prompt = ChatPromptTemplate.from_messages([
        ('system', '당신은 주거지원 조언자 입니다. 사용자의 질문에 아래 참고 문서를 바탕으로 답변해주세요.'),
        *tuple_fewshow_examples,
        MessagesPlaceholder(variable_name='history'),
        ('human', "질문:{question} \n\n 참고 문서\n{context}")
    ])

    chain = prompt | llm | output_parser
    return chain, retriever

def get_answer(chain, retriever, query, history):
    context_docs = retriever.invoke(query)
    llm_answer = chain.invoke({
        "question" : query,
        "context" : '\n\n'.join([doc.page_content for doc in context_docs]),
        "history" :  history
    })
    return llm_answer

def get_answer_stream(chain, retriever, query, history):
    context_docs = retriever.invoke(query)
    llm_answer = chain.stream({
        "question" : query,
        "context" : '\n\n'.join([doc.page_content for doc in context_docs]),
        "history" :  history
    })
    return llm_answer

# %%
