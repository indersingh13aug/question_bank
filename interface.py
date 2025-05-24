# app/ui/interface.py
import gradio as gr
from generator import generate_mcq
iface = gr.Interface(
    fn=generate_mcq,
    inputs=[
        gr.File(label="Upload File (.txt, .docx, .pdf)", file_types=[".txt", ".docx", ".pdf"]),
        gr.Dropdown(choices=["simple", "hard"], label="Select Complexity")
    ],
    outputs=gr.Textbox(label="Generated MCQs"),
    title="MCQ Generator from File",
    description="Upload a file and select the complexity level to generate MCQs using a HuggingFace LLM."
)

if __name__ == "__main__":
    iface.launch()
