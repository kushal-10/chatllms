# Application file for Gradio App for OpenAI Model

import gradio as gr
import time
import datetime
import os

from lc_base.chain import openai_chain
from driveapi.drive import upload_chat_to_drive
from driveapi.drive_database import create_chroma_db

# global time_diff, model_name, search_type
time_diff = 0
# model_name="gpt-3.5-turbo-1106"
model_name = "gpt-4-1106-preview"
search_type = "stuff"
input_question = ""
model_response = ""
user_feedback = ""

dir = ""
title = """<h1 align="center">ResearchBuddy</h1>"""
description = """<br><br><h3 align="center">This is a GPT based Research Buddy to assist in navigating new research topics.</h3>"""

def save_api_key(api_key):
    os.environ['OPENAI_API_KEY'] = str(api_key)
    return f"API Key saved in the environment: {api_key}"

def save_drive_link(drive_link):
    os.environ['DRIVE_LINK'] = str(drive_link)
    print(f"API Key saved in the environment: {drive_link}")
    return None

def create_data_from_drive():
    global db
    db = create_chroma_db()
    return "Processing Completed"

def user(user_message, history):
    return "", history + [[user_message, None]]

def respond(message, chat_history):

    global time_diff, model_response, input_question

    print("Database is ...................")
    print(type(db))
    question = str(message)
    chain = openai_chain(inp_dir=dir)
    
    start_time = time.time()

    output = chain.get_response_from_drive(query=question, database=db, k=10, model_name=model_name, type=search_type)
    print(output)

    # Update global variables to log
    time_diff = time.time() - start_time
    model_response = output
    input_question = question
    
    bot_message = output
    chat_history.append((message, bot_message))

    time.sleep(2)
    return " ", chat_history

def save_feedback(feedback):
    global user_feedback
    user_feedback = feedback

    curr_date = datetime.datetime.now()
    file_name = f"chat_{curr_date.day}_{curr_date.month}_{curr_date.hour}_{curr_date.minute}.csv"
    log_data = [
        ["Question", "Response", "Model", "Time", "Feedback"],
        [input_question, model_response, model_name, time_diff, user_feedback]
    ]

    if user_feedback == "Yes" or  feedback == "No":
        upload_chat_to_drive(log_data, file_name)

def default_feedback():
    return "🤔"

first_message = True

with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald", neutral_hue="slate")) as chat:
    gr.HTML(title)

    global db

    with gr.Row():
        with gr.Column(scale=2):
            api_key_input = gr.Textbox(lines=1, label="Enter your OpenAI API Key, then press Enter...")

        with gr.Column(scale=2):
            drive_link_input = gr.Textbox(lines=1, label="Enter your shared drive link, then press Enter...")

        with gr.Column(scale=1):
            process_files_input = gr.Button(value="Process files")   

    with gr.Row():
        status_message = gr.Text()
    
    api_key_input.submit(save_api_key, [api_key_input])
    drive_link_input.submit(fn=save_drive_link, inputs=[drive_link_input])
    drive_link_check = os.environ.get("DRIVE_LINK")
    process_files_input.click(fn=create_data_from_drive, outputs=status_message)

    chatbot = gr.Chatbot(height=750)
    msg = gr.Textbox(label="Send a message", placeholder="Send a message",
                             show_label=False, container=False)  

    with gr.Row():
        with gr.Column():
            gr.Examples([
                ["Explain these documents to me in simpler terms."],
                ["What does these documents talk about?"],

            ], inputs=msg, label= "Click on any example to copy in the chatbox"
            )

        with gr.Column():
            feedback_radio = gr.Radio(
                choices=["Yes", "No", "🤔"],
                value=["🤔"],
                label="Did you like the latest response?",
                info="Selecting Yes/No will send the following diagnostic data - Question, Response, Time Taken",
            )


    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(default_feedback, outputs=[feedback_radio])
    

    feedback_radio.change(
        fn=save_feedback,
        inputs=[feedback_radio]
    )

    gr.HTML(description)


chat.queue()
chat.launch()
