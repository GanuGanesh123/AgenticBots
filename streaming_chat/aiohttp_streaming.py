import asyncio
import aiohttp
import json
import os
email_text = """My name is Rohan and I am a Staffing Specialist at NextGen Technologies Inc. I am reaching out to you on an exciting job opportunity with one of our clients. Please have a look at the below job description and share your Resume along with the link to the LINKEDIN PROFILE, if you would like to know more about the role.

   

Role: Prompt Engineer

Location: Houston, Texas

Duration: Long Term Contract

 

Job description:

We are seeking a skilled Prompt Engineer to join our team. As a Prompt Engineer, you will be responsible for developing and optimizing prompt structures for various AI models, ensuring that they perform at their best across different applications. You will work closely with our GenAI Engineers to ensure seamless integration and optimization of AI models.

 

Key Responsibilities

Prompt Design: Develop and optimize prompt structures for multiple AI models (e.g., GPT, GEMINI, etc.), ensuring they are tailored to specific use cases.

Model Understanding: Work with data scientists and engineers to understand the unique requirements of different models and design prompts that maximize their performance.

AI Model Integration: Collaborate with other engineering teams to integrate and test prompts within various AI-driven applications.

Optimization: Continuously analyze and improve the effectiveness of prompts through testing and iterative improvements.

Documentation: Document prompt structures, models, and best practices to ensure scalability and knowledge sharing.

 

Required Skills and Qualifications

Experience: 2+ years of experience in prompt engineering, natural language processing, or related AI fields.

Technical Expertise: Deep understanding of prompting structures for AI models and experience working with large language models (LLMs) like GPT, GEMINI, etc.

Programming: Proficiency in Python and AI-related libraries (TensorFlow, PyTorch, etc.).

AI Tools: Familiarity with AI platforms and tools for model orchestration and testing (e.g., Google ADK, LangChain, etc.).

Cloud Platform: GCP, Azure.

Problem-Solving: Strong problem-solving skills and the ability to develop innovative prompt strategies to optimize model performance.

 

Should you be interested, please send me a copy of your resume along with the LinkedIn link ASAP.

 

 

Thanks & Regards

 

Rohan Dhaliwal

Contact: - (669) 333-3067 |Email – rohan@nextgentechinc.com

NextGen Technologies Inc."""
user_prompt = f"""You are email sumarizer assistant. You will be provided with an email text and summarize the email in a concise way. Here is the email text: {email_text}"""



async def stream_gemini_response(api_key: str, prompt: str):
    """
    Makes an asynchronous streaming POST call to the Gemini API.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "stream": True  # Enable streaming
        }
    }

    async with aiohttp.ClientSession(trust_env=True) as session:
        try:
            async with session.post(url, headers=headers, json=payload, ssl=False) as response:
                response.raise_for_status()  # Raise an exception for bad status codes

                print("Streaming response from Gemini API:")
                async for chunk in response.content.iter_chunks():
                    # Each chunk might contain multiple JSON objects
                    # Need to handle potential incomplete JSON objects at chunk boundaries
                    try:
                        decoded_chunk = chunk[0].decode('utf-8')
                        # Gemini API often returns multiple JSON objects per chunk,
                        # separated by newline characters. Split and process each.
                        for line in decoded_chunk.splitlines():
                            if line.strip(): # Ensure line is not empty
                                data = json.loads(line)
                                if 'candidates' in data and data['candidates']:
                                    for candidate in data['candidates']:
                                        if 'content' in candidate and 'parts' in candidate['content']:
                                            for part in candidate['content']['parts']:
                                                if 'text' in part:
                                                    print(part['text'], end='') # Print without newline for continuous text
                    except json.JSONDecodeError as e:
                        print(f"JSON Decode Error: {e} - Partial data: {chunk[0].decode('utf-8', errors='ignore')}")
                    except Exception as e:
                        print(f"Error processing chunk: {e}")

        except aiohttp.ClientError as e:
            print(f"Aiohttp Client Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Replace with your actual Gemini API key
    GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]
    asyncio.run(stream_gemini_response(GEMINI_API_KEY, user_prompt))
