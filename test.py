import torch

# Use a pipeline as a high-level helper
from transformers import pipeline
# import huggingface_hub
import os

# print(os.getenv("HUGGING_FACE_API_KEY"))
# exit()

# huggingface_hub.set_auth_token(os.getenv("HUGGING_FACE_API_KEY"))
pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B", token="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")

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

terminators = [
    pipe.tokenizer.eos_token_id,
    pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = pipe(
    messages,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
)
assistant_response = outputs[0]["generated_text"][-1]["content"]
print(assistant_response)
