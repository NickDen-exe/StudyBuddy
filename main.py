from app.vectorstore import search

results = search("Why does student concentration decline during a lecture, and what can lecturers do about it?")
print(results)