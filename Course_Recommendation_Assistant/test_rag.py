from rag_engine import recommend_course

question = (
    "I am an SAP ABAP developer with no AI experience. "
    "Which course should I take first?"
)

response = recommend_course(question)

print(response)