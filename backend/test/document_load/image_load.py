# from langchain_community.document_loaders import UnstructuredImageLoader

# loader = UnstructuredImageLoader("image.png")

# documents = loader.load()

# print(documents[0].page_content)

# ! ocr with  extract text from image
# import pytesseract
# from PIL import Image

# image = Image.open("image.png")

# text = pytesseract.image_to_string(image)

# print(text)