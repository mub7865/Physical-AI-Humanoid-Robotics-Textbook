import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def simplify_text(text):
    prompt = f"""
    Rewrite the following text for a beginner to intermediate audience.
    Include real-world analogies, simplify jargon, and generate 3-5 key takeaways
    and 2-3 quiz questions.

    Original Text:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o",  # or another suitable model
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    sample_text = "The quantum entanglement phenomenon describes how two particles can become linked..."
    simplified_content = simplify_text(sample_text)
    print(simplified_content)