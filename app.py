# Application file for Gradio App for OpenAI Model

#options - 'output_reports/reports_n/faiss_index' - n=1..9 OR 'combined/faiss_index'
dir = 'combined/faiss_index'

demo_query = "What important topics are discussed in this report?"

import gradio as gr
import time
import pandas as pd
from lc_base.chain import openai_chain

title = """<h1 align="center">Chat</h1>"""
description = """<br><br><h3 align="center">This is a literature chat model, which can currently answer questions to New Data provided.</h3>"""

def user(user_message, history):
    return "", history + [[user_message, None]]

def respond(message, chat_history):
    question = str(message)
    chain = openai_chain(inp_dir=dir)
    output = chain.get_response(query=question, k=20)

    splits = dir.split("/")
    pdf_dir = "data_" + splits[0] + "/data_" + splits[1]
    name = pdf_dir
    store_data = {
        "query" : question,
        "paper" : name,
        "response" : output
    }
    data_df = pd.DataFrame(store_data, index=[0])
    data_df.to_csv("csvs/" + splits[1] + ".csv")

    bot_message = output
    chat_history.append((message, bot_message))
    time.sleep(2)
    return " ", chat_history

with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald", neutral_hue="slate")) as chat:
    gr.HTML(title)
    chatbot = gr.Chatbot().style(height=750)
    msg = gr.Textbox(label="Send a message", placeholder="Send a message",
                             show_label=False).style(container=False)

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    gr.Examples([
        ["What are the challenges and opportunities of AI in supply chain management?"],
        ["What does this report talk about?"],
        ["Explain the key points of this report in detail."],
        ["What is the impact of using AI in supply chain management?"]

    ], inputs=msg, label= "Click on any example to copy in the chatbox"
    )

    gr.HTML(description)


chat.queue()
chat.launch()
