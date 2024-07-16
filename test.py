from PIL import Image
import requests
from transformers import AutoProcessor, LlavaForConditionalGeneration
import torch

print('starting test program...')
print('loading llava model...')
model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf", torch_dtype=torch.float16, device_map="auto")

print('loading processor...')
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")

print('loading image...')
prompt = "USER: <image>\nWhat's the content of the image? ASSISTANT:"
url = "https://www.ilankelman.org/stopsigns/australia.jpg"
image = Image.open(requests.get(url, stream=True).raw)

print('processor generating inputs...')
inputs = processor(text=prompt, images=image, return_tensors="pt")

# Generate
print('model generating outputs...')
generate_ids = model.generate(**inputs, max_new_tokens=15)
print('processor decoding outputs...')
print(processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])