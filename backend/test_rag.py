from app.services.rag_service import answer_query


answer = answer_query(
    "What percentage of the eligible lodging amount can an employee claim when staying at a relative or friend's home?"
)

print("\nAnswer:")
print(answer)