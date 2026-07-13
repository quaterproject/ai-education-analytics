from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("sample.pdf")

documents = loader.load()

print(documents[0].page_content)