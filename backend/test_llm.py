from app.generation.llm import generate_answer


answer = generate_answer(
    "Explain what a vector embedding is in one sentence."
)

print(answer)