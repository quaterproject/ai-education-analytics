from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="data.csv",
    encoding="utf-8"
)

documents = loader.load()

print(documents[0].page_content)