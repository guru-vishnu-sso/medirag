def chunk_text(pages, chunk_size=500, overlap=100):
    """
    Split each PDF page into overlapping chunks
    while preserving the page number.

    Args:
        pages: List of dictionaries
               [
                   {"page": 1, "text": "..."},
                   {"page": 2, "text": "..."}
               ]

    Returns:
        List of dictionaries
        [
            {
                "page": 1,
                "text": "chunk..."
            }
        ]
    """

    chunks = []

    for page in pages:

        page_number = page["page"]
        text = page["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append(
                {
                    "page": page_number,
                    "text": chunk
                }
            )

            start += chunk_size - overlap

    return chunks