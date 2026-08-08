from app.vectorstore import search
from app.llm import ask_llm

PROMPT_TEMPLATE = (
    "You are a helpful assistant answering questions based on lecture materials.\n\n"
    "Context from lecture materials:\n{context}\n\n"
    "Question: {question}\n\n"
    "Instructions:\n"
    "1. First, try to answer the question using ONLY the context above.\n"
    "2. If the context contains a direct answer, answer clearly and concisely, "
    "citing which source it came from.\n"
    "3. If the context does NOT contain a direct answer, you may answer using "
    "your own general knowledge, but you MUST start your answer with: "
    "\"I couldn't find a direct answer in the lecture materials, so here's what "
    "I know generally:\" before giving that answer."
)


def format_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    formatted_context = [
        f"Source: {meta['source']}, Location: {meta['location']}, Content: {doc}"
        for doc, meta in zip(documents, metadatas)
    ]

    return "\n".join(formatted_context)


def generate_answer(query):
    search_results = search(query)
    context = format_context(search_results)
    prompt = PROMPT_TEMPLATE.format(context=context, question=query)
    answer = ask_llm(prompt)
    return answer