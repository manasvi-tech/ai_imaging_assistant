import os
import google.generativeai as genai

# Hardcode your actual API key here
genai.configure(api_key="AIzaSyDXBfYYm4G1VS9er2uR2uk_JDfKpBLTEQs")

model = genai.GenerativeModel("gemini-1.5-pro")

response = model.generate_content("Say hello from Gemini.")
print(response.text)