from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model


from config import BASE_URL, API_KEY, MODEL
from rich import print
llm = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,  # If you prefer to pass api key in directly
    base_url=BASE_URL,
    # stream_usage=True,
    # temperature=None,
    # max_tokens=None,
    # timeout=None,
    # reasoning_effort="low",
    # max_retries=2,
    # organization="...",
    # other params...
)

llm2 = init_chat_model(
    model_provider="openai",
    model=MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
)


if __name__ == "__main__":
    res = llm2.invoke("Hello, how are you?")
    print(res)