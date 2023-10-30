from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS 
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

import os 
os.environ["OPENAI_API_KEY"] = "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"

class openai_chain():
    def __init__(self, inp_dir='output_reports/reports_1/faiss_index') -> None:
        self.inp_dir = inp_dir
        pass

    def get_response(self, query, k=3, type="map_reduce"):
        # Initialize OPENAI embeddings
        embedding = OpenAIEmbeddings()

        # Load Database for required PDF
        db = FAISS.load_local(self.inp_dir, embedding)

        # Get relevant docs
        docs = db.similarity_search(query, k=k)

        # Create Chain
        chain = load_qa_chain(ChatOpenAI(model="gpt-3.5-turbo"), chain_type=type)

        # Get Response
        response = chain.run(input_documents=docs, question=query)

        return response


        
"""
TODO 

1) Map_Reduce - 7 mins just to process a 27 page report
1.5) Map_reduce on smaller reports - 
2) Stuff - 30 secs to process and give the output

Check condition? <4K use #stuff else use #Map_reduce

Potential  Errors

Explain the key points of this report in detail.

I'm sorry, but I can't provide a detailed explanation of the key points of the report as the relevant portion of the document you provided does not contain any specific information about the report or its key points. It mainly talks about the services provided by Boston Consulting Group (BCG) and how they aim to help clients and make a positive impact in the world. If you have access to the full report, please provide more specific information or context, and I'll be happy to assist you further.

Preprocess data - remove \n or blank spaces


def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie

llmsherpa -> nlmatics for PDF reading into subsections
Use GPT-4? -> check speed
Use two modes -> summarizer wholedoc + chat top3doc

compare summarizing answers by stuff and map_reduce

use top6 across the paper -> 500 each
"""
