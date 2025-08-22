from langchain_google_genai import ChatGoogleGenerativeAI
import os
import sys
import pandas as pd
import io


sys.path.append("../../")
from utils.file_utils import load_text_file_as_string
# Set your API key as an environment variable or pass it directly
#os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

# Load prompt string

def postprocess(llm_response):
    # conver to csv and save locally
    output_df = pd.read_csv(io.StringIO(llm_response))
    output_df.to_csv("domain_classifications.csv", index=False)

prompt_template = load_text_file_as_string("prompt.txt")

list_of_domains = ["facebook.com", "gulte.com"]

final_prompt = f'{prompt_template} \n ["facebook.com", "gulte.com"]'

print("Internal prompt template: \n")
print(final_prompt)

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", temperature=0.7) 
# You can choose other models like "gemini-pro-vision" for multimodal tasks
# and adjust parameters like 'temperature' for creativity.

response = llm.invoke(final_prompt)
print("\n\nSaving LLM Response: ")
#print(response.content)
postprocess(response.content)






