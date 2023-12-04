# Application file for Gradio App for OpenAI Model

import gradio as gr
import time
from lc_base.chain import openai_chain
import os
from lc_base.logs import save_log

dir = os.path.join("outputs", "combined", "policy_eu_asia", "faiss_index")
# dir = os.path.join("outputs", "policy", "1", "faiss_index")

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
    start_time = time.time()
    output = chain.get_response(query=question, k=100, model_name="gpt-4-1106-preview", type="stuff")
    print(output)
    time_taken = time.time() - start_time
    save_log(file_path='logs/policy_combined.csv', query=question, response=output, model_name="gpt-4-1106-preview", time_taken=time_taken, inp="Policy", data="Policy/1")
    bot_message = output
    chat_history.append((message, bot_message))
    time.sleep(2)
    return " ", chat_history

with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald", neutral_hue="slate")) as chat:
    gr.HTML(title)
                 
    api_key_input = gr.Textbox(lines=1, label="Enter your OpenAI API Key")
    api_key_input_submit = api_key_input.submit(save_api_key, [api_key_input])

    chatbot = gr.Chatbot(height=750)
    msg = gr.Textbox(label="Send a message", placeholder="Send a message",
                             show_label=False, container=False)

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    gr.Examples([
        ["What are the challenges and opportunities of AI in supply chain management?"],
        ["What does these documents talk about?"],

    ], inputs=msg, label= "Click on any example to copy in the chatbox"
    )

    gr.HTML(description)


chat.queue()
chat.launch()
