from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich import print


document = "LangChain is the framework for building context-aware reasoning applications. It provides tools and abstractions to help developers create applications that can reason over text, code, and other data sources. With LangChain, you can build applications that understand context, perform complex reasoning, and generate human-like responses."

text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
texts = text_splitter.split_text(document)


if __name__ == "__main__":

    for i, text in enumerate(texts):
        print(f"Chunk {i + 1}: {text}")
