# Application file for Gradio App for OpenAI Model

import gradio as gr
import time
import pandas as pd
from lc_base.chain import openai_chain
import os
import requests

dir = os.path.join("outputs", "combined", "papers_gpt4turbo_mapred5", "faiss_index")

title = """<h1 align="center">Chat</h1>"""
description = """<br><br><h3 align="center">This is a literature chat model, which can currently answer questions to New Data provided.</h3>"""

def save_api_key(api_key):
    os.environ['OPENAI_API_KEY'] = str(api_key)
    return f"API Key saved in the environment: {api_key}"

def user(user_message, history):
    return "", history + [[user_message, None]]

def respond(message, chat_history):
    question = str(message)
    chain = openai_chain(inp_dir=dir)
    output = chain.get_response(query=question, k=1, model_name="gpt-3.5-turbo", type="stuff")

    bot_message = output
    chat_history.append((message, bot_message))
    time.sleep(2)
    return " ", chat_history

with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald", neutral_hue="slate")) as chat:
    gr.HTML(title)
                 
    api_key_input = gr.Textbox(lines=1, label="Enter your OpenAI API Key")
    api_key_input_submit = api_key_input.submit(save_api_key, [api_key_input])

    chatbot = gr.Chatbot().style(height=750)
    msg = gr.Textbox(label="Send a message", placeholder="Send a message",
                             show_label=False).style(container=False)

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    gr.Examples([
        ["What are the challenges and opportunities of AI in supply chain management?"],
        ["What does these reports talk about?"],
        ["What does these papers talk about? Please explain in detail."],
        ["What is the impact of using AI in supply chain management?"]

    ], inputs=msg, label= "Click on any example to copy in the chatbox"
    )

    gr.HTML(description)


chat.queue()
chat.launch()
