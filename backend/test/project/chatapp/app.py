from chains import (
    reasoning_chain,
    summary_chain,
    explanation_chain,
    report_chain,
)
from rich import print

print("Choose a task:")
print("1. Reasoning")
print("2. Summarization")
print("3. Explanation")
print("4. Report Generation")

choice = input("Enter choice: ")

if choice == "1":
    question = input("Question: ")
    result = reasoning_chain.invoke({"question": question})

elif choice == "2":
    text = input("Text: ")
    result = summary_chain.invoke({"text": text})

elif choice == "3":
    concept = input("Concept: ")
    result = explanation_chain.invoke({"concept": concept})

elif choice == "4":
    content = input("Content: ")
    result = report_chain.invoke({"content": content})

else:
    print("Invalid choice")
    exit()

print("\nResult:\n")
print(result.content)