import sys
import os

# Adds the root project folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# from langchain_openai import ChatOpenAI
from test.models.chatmodel import llm
from prompts import (
    reasoning_prompt,
    summary_prompt,
    explanation_prompt,
    report_prompt,
)

# llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

reasoning_chain = reasoning_prompt | llm
summary_chain = summary_prompt | llm
explanation_chain = explanation_prompt | llm
report_chain = report_prompt | llm