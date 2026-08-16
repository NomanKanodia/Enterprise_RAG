from app.services.rag_service import answer_query


answer = answer_query(
    "When did the Travel Policy come into effect?"
)

print("\nAnswer:")
print(answer)