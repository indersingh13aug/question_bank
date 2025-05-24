# app/ui/interface.py
import gradio as gr
from generator import generate_mcq, summarize_text

def run_mcq(file, complexity, content_type):
    return generate_mcq(file, complexity, content_type)

def run_summary(file, content_type):
    return summarize_text(file, content_type)

with gr.Blocks() as iface:
    gr.Markdown("MCQ and Summary Generator")
    gr.Markdown("Upload a file, choose the complexity, mention content type, and generate MCQs or a short summary.")

    with gr.Row():
        file_input = gr.File(label="Upload File (.txt, .docx, .pdf)", file_types=[".txt", ".docx", ".pdf"])
        complexity = gr.Dropdown(choices=["simple", "hard"], label="Select Complexity")
        content_type = gr.Textbox(label="Content Type (e.g., History chapter, Science article)")

    with gr.Row():
        generate_btn = gr.Button("Generate MCQs")
        summarize_btn = gr.Button("Summarize (~100 words)")

    mcq_output = gr.Textbox(label="Generated MCQs")
    summary_output = gr.Textbox(label="Summary (100 words)")

    generate_btn.click(run_mcq, inputs=[file_input, complexity, content_type], outputs=mcq_output)
    summarize_btn.click(run_summary, inputs=[file_input, content_type], outputs=summary_output)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
