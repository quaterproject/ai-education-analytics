from langchain_core.prompts import ChatPromptTemplate

reasoning_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert reasoning assistant."),
    ("human", "{question}")
])

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the following text in a concise way."),
    ("human", "{text}")
])

explanation_prompt = ChatPromptTemplate.from_messages([
    ("system", "Explain the following concept clearly for beginners."),
    ("human", "{concept}")
])

report_prompt = ChatPromptTemplate.from_messages([
    ("system", "Generate a professional report from the provided information."),
    ("human", "{content}")
])