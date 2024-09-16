from langchain_ollama import OllamaLLM


model = OllamaLLM(model="llama3")

result = model.invoke(input="Tell me about Zilina")

print(result)
