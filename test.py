# from langchain_ollama import OllamaLLM
#
#
# model = OllamaLLM(model="llama3")
#
# result = model.invoke(input="Tell me about Zilina")
#
# print(result)

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
