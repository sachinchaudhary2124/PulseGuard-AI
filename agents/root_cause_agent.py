import os
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()


# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_root_cause(anomaly):
    """
    Analyze anomaly using OpenAI.
    """

    prompt = f"""
    You are an expert Site Reliability Engineer (SRE).

    Analyze the following API anomaly and explain:

    1. Probable root cause
    2. Business impact
    3. Recommended fix

    Anomaly Details:
    {anomaly}
    """

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI observability engineer."
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
        return f"❌ AI Analysis Error: {e}"