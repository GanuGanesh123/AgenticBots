import requests
import json
import asyncio
import google.generativeai as genai
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



google_api_key = os.environ["GOOGLE_API_KEY"]


# Configure your API key
# Replace "YOUR_API_KEY" with your actual Gemini API key
genai.configure(api_key=google_api_key)

async def stream_gemini_response(prompt: str):
    """
    Sends an asynchronous POST request to the Gemini API with streaming
    and prints the streamed content.
    """
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
    
    print(f"Sending prompt: '{prompt}'")
    
    # Use stream=True to enable streaming
    response_stream = await model.generate_content_async(
        contents=prompt,
        stream=True
    )

    print("Streaming response:")
    async for chunk in response_stream:
        print(chunk.text, end='') # Print each chunk as it arrives

async def main():
    await stream_gemini_response(user_prompt)

if __name__ == "__main__":
    asyncio.run(main())