from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS 
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

class openai_chain():
    def __init__(self, inp_dir='output_reports/reports_1/faiss_index') -> None:
        self.inp_dir = inp_dir
        pass

    def get_response(self, query, k=3, type="map_reduce", model_name="gpt-3.5-turbo"):
        # Initialize OPENAI embeddings
        embedding = OpenAIEmbeddings()

        # Load Database for required PDF
        db = FAISS.load_local(self.inp_dir, embedding)

        # Get relevant docs
        docs = db.similarity_search(query, k=k)

        # Create Chain
        chain = load_qa_chain(ChatOpenAI(model=model_name), chain_type=type)

        # Get Response
        response = chain.run(input_documents=docs, question=query)

        return response

    def get_response_from_drive(self, query, database, k=3, type="stuff", model_name="gpt-3.5-turbo"):
        # Get relevant docs
        docs = database.similarity_search(query, k=k)

        # Create chain
        chain = load_qa_chain(ChatOpenAI(model=model_name), chain_type=type)

        #Get Response
        response = chain.run(input_documents=docs, question=query)
        
        return response