from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter_var = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap  = 40,
    length_function = len,
    separators= ["\n", "\\n", "\n\n", ".", "!", "?", "/", "\\"]
)

def text_splitter(text):
    return text_splitter_var.split_text(text)