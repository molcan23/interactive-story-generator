# Use a pipeline as a high-level helper
from transformers import pipeline
from dotenv import load_dotenv
import torch
import os

load_dotenv()  # This will load the environment variables from the .env file

pipe = pipeline(
    "text-generation",
    model_kwargs={"torch_dtype": torch.bfloat16},
    model="meta-llama/Meta-Llama-3-8B",
    token=os.getenv("HUGGING_FACE_API_KEY")
)

chat_template = """
[USER_ROLE] "{USER_CONTENT}"
[ASSISTANT_ROLE] "{ASSISTANT_CONTENT}"
"""

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

terminators = [
    pipe.tokenizer.eos_token_id,
    pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = pipe(
    messages
)

assistant_response = outputs[0]["generated_text"][-1]["content"]

print(assistant_response)
