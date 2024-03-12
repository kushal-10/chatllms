# Application file for Gradio App for OpenAI Model

import gradio as gr
import time
import datetime
import os

from lc_base.chain import openai_chain
from lc_base.dnd_database import create_dnd_database
from driveapi.drive import upload_chat_to_drive
from driveapi.drive_database import create_chroma_db

# global time_diff, model_name, search_type
time_diff = 0
# model_name="gpt-3.5-turbo-1106" # FOR TESTING
# model_name = "gpt-4-1106-preview"https://huggingface.co/spaces/Koshti10/Chat_literature/edit/main/app_drive.py
model_name = "gpt-4-0125-preview"
search_type = "stuff"
input_question = ""
model_response = ""
user_feedback = ""

dir = ""
title = """<h1 align="center">ResearchBuddy</h1>"""
description = """<br><br><h3 align="center">This is a GPT based Research Buddy to assist in navigating new research topics.</h3>"""


def save_drive_link(drive_link):
    drive_link += "?usp=sharing"
    os.environ['DRIVE_LINK'] = str(drive_link)
    print("Drive link saved in the environment")
    return None

def create_data_from_drive(drive_link):
    global db

    drive_link += "?usp=sharing"
    os.environ['DRIVE_LINK'] = str(drive_link)
    print("Drive link saved in the environment! Creating Database...")

    db = create_chroma_db()
    return "Processing Completed - You can start the chat now!"

def check_pdfs(pdf_files):
    global db
    db = create_dnd_database(pdf_files)
    return "Processing Completed - You can start the chat now!"

def user(user_message, history):
    return "", history + [[user_message, None]]

def respond(message, chat_history):

    global time_diff, model_response, input_question

    print("Database is ...................")
    print(type(db))
    question = str(message)
    chain = openai_chain(inp_dir=dir)

    query = question

    start_time = time.time()

    output = chain.get_response_from_drive(query=query, database=db, k=10, model_name=model_name, type=search_type)
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
    file_name = f"chat_{curr_date.day}_{curr_date.month}_{curr_date.hour}_{curr_date.minute}_{curr_date.second}.csv"
    log_data = [
        ["Question", "Response", "Model", "Time", "Feedback"],
        [input_question, model_response, model_name, time_diff, user_feedback]
    ]
    
    if model_response and user_feedback[0] != "None":
        upload_chat_to_drive(log_data, file_name)


def default_feedback():
    return "None"

def default_text():
    return ""

def text_feedback(feedback):
    global text_feedback
    text_feedback = feedback

    curr_date = datetime.datetime.now()
    file_name = f"chat_{curr_date.day}_{curr_date.month}_{curr_date.hour}_{curr_date.minute}_{curr_date.second}.csv"
    log_data = [
        ["Question", "Response", "Model", "Time", "Feedback"],
        [input_question, model_response, model_name, time_diff, text_feedback]
    ]

    upload_chat_to_drive(log_data, file_name)

with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald", neutral_hue="slate")) as chat:
    gr.HTML(title)

    global db

    with gr.Row(equal_height=True):
        with gr.Column():
            with gr.Row():
                pdf_files_dnd = gr.File(file_count='multiple', height=250, label="Upload PDF Files")


        with gr.Column():
           with gr.Row():
                drive_link_input = gr.Textbox(lines=1, label="Enter your shared drive link, then press Enter...")
           with gr.Row():
                status_message = gr.Text(label="Status", value="⬆️Submit a (shared) drive link containing only PDFs \n-or- \n⬅️Upload PDF files", text_align='center')
            

        
        

    drive_link_input.submit(fn=create_data_from_drive, inputs=[drive_link_input], outputs=[status_message])
    pdf_files_dnd.change(fn=check_pdfs, inputs=[pdf_files_dnd], outputs=[status_message], preprocess=False, postprocess=False)

    chatbot = gr.Chatbot(height=750)
    msg = gr.Textbox(label="Send a message", placeholder="Send a message",
                             show_label=False, container=False)  

    with gr.Row():
        with gr.Column():
            gr.Examples([
                ["Explain these documents to me in simpler terms."],
                ["What does these documents talk about?"],
                ["Give the key topics covered in these documents in less than 10 words."],
                ["What are the key findings in these documents?"],
            ], inputs=msg, label= "Click on any example to copy in the chatbox"
            )

    with gr.Row():
        with gr.Column():
            feedback_radio = gr.Radio(
                choices=["1", "2", "3", "4", "5", "6", "None"],
                value=["None"],
                label="On a scale from 1 (very unsatisfied) to 6 (very satisfied), how would you rate the current response?",
                )
        
        with gr.Column():
            feedback_text = gr.Textbox(lines=1, label="Additional comments on the current response...")


    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(default_feedback, outputs=[feedback_radio])
    chatbot.change(save_feedback, inputs=[feedback_radio])

    feedback_radio.change(
        fn=save_feedback,
        inputs=[feedback_radio]
    )

    feedback_text.submit(
        fn=text_feedback,
        inputs=[feedback_text]
    )

    feedback_text.submit(
        fn=default_text,
        outputs=[feedback_text]
    )

    gr.HTML(description)


chat.queue()
chat.launch()