from app.services.rag_service import answer_query


answer = answer_query(
    "How many pages long is the PDF?"
)

print("\nAnswer:")
print(answer)