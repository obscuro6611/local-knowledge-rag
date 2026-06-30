import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from document_loader import load_documents
from chunker import create_chunks
from embedding_engine import (
    create_embeddings,
    MODEL_NAME
)
from retrieval_engine import retrieve_chunks
from vector_store import (
    save_vector_store,
    vector_store_exists
)
from llm_engine import generate_answer
from export_engine import export_answer


KB_INFO_PATH = Path(
    "knowledge_base/kb_info.json"
)


class LocalKnowledgeRAGApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Local Knowledge RAG"
        )

        self.root.geometry(
            "1600x1000"
        )

        self.selected_folder = ""

        self.documents = []
        self.chunks = []
        self.embeddings = None

        self.current_question = ""
        self.current_sources = []
        self.current_answer = ""

        title = tk.Label(
            root,
            text="Local Knowledge RAG",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        controls_frame = tk.Frame(root)
        controls_frame.pack(pady=5)

        self.select_button = tk.Button(
            controls_frame,
            text="Select Knowledge Folder",
            command=self.select_folder,
            width=25
        )
        self.select_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=2
        )

        self.load_button = tk.Button(
            controls_frame,
            text="Load Documents",
            command=self.load_documents_from_folder,
            width=25
        )
        self.load_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=2
        )

        self.chunk_button = tk.Button(
            controls_frame,
            text="Create Chunks",
            command=self.create_document_chunks,
            width=25
        )
        self.chunk_button.grid(
            row=1,
            column=0,
            padx=5,
            pady=2
        )

        self.embedding_button = tk.Button(
            controls_frame,
            text="Create Embeddings",
            command=self.create_chunk_embeddings,
            width=25
        )
        self.embedding_button.grid(
            row=1,
            column=1,
            padx=5,
            pady=2
        )

        self.save_button = tk.Button(
            controls_frame,
            text="Save Knowledge Base",
            command=self.save_knowledge_base,
            width=25
        )
        self.save_button.grid(
            row=2,
            column=0,
            padx=5,
            pady=2
        )

        self.ask_button = tk.Button(
            controls_frame,
            text="Ask Question",
            command=self.ask_question,
            width=25
        )
        self.ask_button.grid(
            row=2,
            column=1,
            padx=5,
            pady=2
        )

        self.export_button = tk.Button(
            controls_frame,
            text="Export Answer",
            command=self.export_current_answer,
            width=25
        )
        self.export_button.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=2
        )

        self.question_entry = tk.Entry(
            root,
            width=120
        )
        self.question_entry.pack(
            pady=10
        )

        self.folder_label = tk.Label(
            root,
            text="No folder selected",
            wraplength=1300,
            justify="left"
        )
        self.folder_label.pack(
            pady=5
        )

        self.document_label = tk.Label(
            root,
            text="Documents Loaded: 0"
        )
        self.document_label.pack()

        self.chunk_label = tk.Label(
            root,
            text="Chunks Created: 0"
        )
        self.chunk_label.pack()

        self.embedding_label = tk.Label(
            root,
            text="Embeddings Created: 0"
        )
        self.embedding_label.pack()

        kb_status = (
            "Knowledge Base Found"
            if vector_store_exists()
            else "No Knowledge Base Found"
        )

        self.kb_label = tk.Label(
            root,
            text=kb_status
        )
        self.kb_label.pack(
            pady=5
        )

        self.kb_info_label = tk.Label(
            root,
            text="Knowledge Base Information",
            justify="left",
            anchor="w",
            font=("Courier New", 10)
        )

        self.kb_info_label.pack(
            pady=5
        )

        self.status_label = tk.Label(
            root,
            text="Status: Ready",
            font=("Arial", 10, "bold")
        )
        self.status_label.pack(
            pady=2
        )

        self.progress_bar = ttk.Progressbar(
            root,
            orient="horizontal",
            length=500,
            mode="determinate"
        )
        self.progress_bar.pack(
            pady=2
        )

        self.progress_label = tk.Label(
            root,
            text="0%"
        )
        self.progress_label.pack(
            pady=2
        )

        content_frame = tk.Frame(root)
        content_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        left_frame = tk.Frame(
            content_frame
        )
        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        right_frame = tk.Frame(
            content_frame
        )
        right_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            left_frame,
            text="Retrieved Sources",
            font=("Arial", 12, "bold")
        ).pack()

        source_scroll = tk.Scrollbar(
            left_frame
        )
        source_scroll.pack(
            side="right",
            fill="y"
        )

        self.sources_text = tk.Text(
            left_frame,
            wrap="word",
            yscrollcommand=source_scroll.set
        )

        self.sources_text.pack(
            fill="both",
            expand=True
        )

        source_scroll.config(
            command=self.sources_text.yview
        )

        tk.Label(
            right_frame,
            text="Answer",
            font=("Arial", 12, "bold")
        ).pack()

        answer_scroll = tk.Scrollbar(
            right_frame
        )
        answer_scroll.pack(
            side="right",
            fill="y"
        )

        self.answer_text = tk.Text(
            right_frame,
            wrap="word",
            yscrollcommand=answer_scroll.set
        )

        self.answer_text.pack(
            fill="both",
            expand=True
        )

        answer_scroll.config(
            command=self.answer_text.yview
        )

        self.load_kb_info()

    def load_kb_info(self):

        if not KB_INFO_PATH.exists():

            self.kb_info_label.config(
                text="Knowledge Base Information\n\nNo metadata found"
            )

            return

        with open(
            KB_INFO_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            info = json.load(file)

        status = (
            "Loaded"
            if vector_store_exists()
            else "Missing"
        )

        info_text = (
            "Knowledge Base Information\n\n"
            f"Documents Indexed : {info.get('documents', 0)}\n"
            f"Chunks Stored     : {info.get('chunks', 0)}\n"
            f"Embedding Model   : {info.get('embedding_model', 'Unknown')}\n"
            f"Last Build Time   : {info.get('last_build_time', 'Unknown')}\n"
            f"Index Status      : {status}"
        )

        self.kb_info_label.config(
            text=info_text
        )

    def set_status(self, message):

        self.status_label.config(
            text=f"Status: {message}"
        )

        self.root.update_idletasks()

    def set_progress(self, value):

        self.progress_bar["value"] = value

        self.progress_label.config(
            text=f"{value:.0f}%"
        )

        self.root.update_idletasks()

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.selected_folder = folder

            self.folder_label.config(
                text=f"Knowledge Folder:\n{folder}"
            )

    def load_documents_from_folder(self):

        self.set_status(
            "Loading Documents..."
        )

        self.documents = load_documents(
            self.selected_folder
        )

        self.document_label.config(
            text=f"Documents Loaded: {len(self.documents)}"
        )

        self.set_status(
            "Ready"
        )

    def create_document_chunks(self):

        self.set_status(
            "Creating Chunks..."
        )

        self.chunks = create_chunks(
            self.documents
        )

        self.chunk_label.config(
            text=f"Chunks Created: {len(self.chunks)}"
        )

        self.set_status(
            "Ready"
        )

    def create_chunk_embeddings(self):

        self.set_status(
            "Generating Embeddings..."
        )

        self.set_progress(0)

        self.embeddings = create_embeddings(
            self.chunks,
            progress_callback=self.set_progress
        )

        self.embedding_label.config(
            text=f"Embeddings Created: {len(self.embeddings)}"
        )

        self.set_progress(100)

        self.set_status(
            "Ready"
        )

    def save_knowledge_base(self):

        self.set_status(
            "Saving Knowledge Base..."
        )

        save_vector_store(
            self.embeddings,
            self.chunks,
            MODEL_NAME
        )

        self.kb_label.config(
            text="Knowledge Base Saved"
        )

        self.load_kb_info()

        self.set_status(
            "Ready"
        )

    def ask_question(self):

        question = self.question_entry.get()

        if not question.strip():
            return

        self.set_status(
            "Retrieving Sources..."
        )

        retrieved_chunks = retrieve_chunks(
            question
        )

        self.sources_text.delete(
            "1.0",
            tk.END
        )

        for i, chunk in enumerate(
            retrieved_chunks,
            start=1
        ):

            self.sources_text.insert(
                tk.END,
                f"\n=== SOURCE {i} ===\n"
            )

            self.sources_text.insert(
                tk.END,
                f"{chunk['filename']}\n\n"
            )

            self.sources_text.insert(
                tk.END,
                chunk["text"]
            )

            self.sources_text.insert(
                tk.END,
                "\n\n"
            )

        self.set_status(
            "Generating Answer..."
        )

        answer = generate_answer(
            question,
            retrieved_chunks
        )

        self.answer_text.delete(
            "1.0",
            tk.END
        )

        self.answer_text.insert(
            tk.END,
            answer
        )

        self.current_question = question
        self.current_sources = retrieved_chunks
        self.current_answer = answer

        self.set_status(
            "Ready"
        )

    def export_current_answer(self):

        if not self.current_answer:

            self.set_status(
                "Nothing to export"
            )

            return

        export_file = export_answer(
            self.current_question,
            self.current_sources,
            self.current_answer
        )

        self.set_status(
            f"Exported: {export_file.name}"
        )


root = tk.Tk()

app = LocalKnowledgeRAGApp(root)

root.mainloop()