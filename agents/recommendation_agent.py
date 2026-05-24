import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_executive_summary(anomalies):

    prompt = f"""
    You are an expert AI Operations Analyst.

    Analyze the following anomalies and generate:

    1. Overall system health summary
    2. Most critical issue
    3. Business risk
    4. Recommended engineering priority

    Anomalies:
    {anomalies}

    Keep the response concise but professional.
    """

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI infrastructure analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Executive Summary Error: {e}"