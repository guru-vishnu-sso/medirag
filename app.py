import streamlit as st
from services.pdf_service import save_uploaded_file
from services.rag_service import (
    process_pdf,
    answer_question
)

st.set_page_config(
    page_title="MediRAG",
    page_icon="🩺",
    layout="wide"
)

# ==========================
# Session State
# ==========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pages" not in st.session_state:
    st.session_state.pages = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "index" not in st.session_state:
    st.session_state.index = None


st.title("🩺 MediRAG")
st.subheader(
    "AI Clinical Knowledge Assistant"
)

pages = st.session_state.pages
chunks = st.session_state.chunks
index = st.session_state.index


# ==========================
# Upload PDF
# ==========================
st.header("📄 Upload Medical Document")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


# ==========================
# Sidebar
# ==========================
with st.sidebar:

    st.title("🩺 MediRAG")

    st.divider()

    if uploaded_file:
        st.success("PDF Uploaded")
    else:
        st.warning("No PDF Uploaded")

    language = st.selectbox(
        "🌐 Answer Language",
        [
            "English",
            "Telugu",
            "Hindi"
        ]
    )

    st.divider()

    generate_summary = st.button(
        "📋 Generate Summary"
    )

    simplify_report = st.button(
        "🏥 Explain Report Simply"
    )

    st.divider()

    chat_text = ""

    for chat in st.session_state.chat_history:

        chat_text += (
            f"Question: "
            f"{chat['question']}\n"
        )

        chat_text += (
            f"Answer: "
            f"{chat['answer']}\n\n"
        )

    st.download_button(
        "📥 Download Chat",
        chat_text,
        file_name="chat_history.txt"
    )

    st.divider()

    clear_chat = st.button(
        "🗑 Clear Chat"
    )

    clear_document = st.button(
        "🗑 Clear Document"
    )


# ==========================
# Clear Buttons
# ==========================
if clear_chat:

    st.session_state.chat_history = []

    st.rerun()

if clear_document:

    st.session_state.pages = None
    st.session_state.chunks = None
    st.session_state.index = None

    st.rerun()


# ==========================
# Process PDF
# ==========================
if uploaded_file is not None:

    file_path = save_uploaded_file(
        uploaded_file
    )

    st.success(
        "PDF uploaded successfully!"
    )

    if st.session_state.index is None:

        with st.spinner(
            "Processing PDF..."
        ):

            pages, chunks, embeddings, index = (
                process_pdf(file_path)
            )

            st.session_state.pages = pages
            st.session_state.chunks = chunks
            st.session_state.index = index

    else:

        pages = st.session_state.pages
        chunks = st.session_state.chunks
        index = st.session_state.index

    st.success(
        "PDF processed successfully!"
    )

    # ======================
    # Sidebar Metrics
    # ======================
    with st.sidebar:

        st.divider()

        st.success(
            "Document Ready"
        )

        st.metric(
            "Pages",
            len(pages)
        )

        st.metric(
            "Chunks",
            len(chunks)
        )

        st.metric(
            "Vectors",
            index.ntotal
        )

        st.write("📄 File")

        st.code(
            uploaded_file.name
        )

    # ======================
    # Preview
    # ======================
    preview = ""

    if isinstance(
        pages,
        list
    ):

        for page in pages[:2]:

            if isinstance(page, dict):

                preview += page["text"]

            else:

                preview += str(page)

    else:

        preview = str(pages)

    st.subheader(
        "📖 Extracted Text Preview"
    )

    st.text_area(
        "First 1000 characters",
        preview[:1000],
        height=300
    )

    # ======================
    # Summary
    # ======================
    if generate_summary:

        with st.spinner(
            "Generating summary..."
        ):

            result = answer_question(
                """
                Summarize this document.

                Include:
                1. Main topics
                2. Important guidelines
                3. Key precautions.
                """,
                index,
                chunks,
                language
            )

        st.subheader(
            "📋 Document Summary"
        )

        st.write(
            result["answer"]
        )

    # ======================
    # Simplifier
    # ======================
    if simplify_report:

        with st.spinner(
            "Simplifying report..."
        ):

            result = answer_question(
                """
                Explain this medical
                document in simple language.

                Include:

                1. Main findings
                2. Important concerns
                3. Explain medical terms
                4. Recommendations
                """,
                index,
                chunks,
                language
            )

        st.subheader(
            "🏥 Simplified Report"
        )

        st.write(
            result["answer"]
        )


st.divider()

# ==========================
# Ask Questions
# ==========================
st.header("💬 Ask PDF")

question = st.text_input(
    "Ask a question from the uploaded PDF"
)

if st.button("Ask PDF"):

    if uploaded_file is None:

        st.error(
            "Please upload a PDF first."
        )

    elif question:

        with st.spinner(
            "Searching..."
        ):

            result = answer_question(
                question,
                index,
                chunks,
                language
            )

        answer = result["answer"]

        retrieved_chunks = (
            result["chunks"]
        )

        st.subheader(
            "🤖 Answer"
        )

        st.write(answer)

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        st.divider()

        st.subheader(
            "📚 Sources Used"
        )

        for i, chunk in enumerate(
                retrieved_chunks
        ):

            page_num = chunk.get(
                "page",
                "Unknown"
            )

            with st.expander(
                f"📄 Source {i+1} "
                f"(Page {page_num})"
            ):

                st.write(
                    chunk["text"]
                )

    else:

        st.warning(
            "Please enter a question."
        )


# ==========================
# Chat History
# ==========================
st.divider()

st.header("💬 Chat History")

for chat in reversed(
        st.session_state.chat_history
):

    with st.chat_message(
            "user"
    ):
        st.write(
            chat["question"]
        )

    with st.chat_message(
            "assistant"
    ):
        st.write(
            chat["answer"]
        )