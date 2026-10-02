"""
VASUKI OpenAI Client Integration Example
Requires: pip install openai
"""
from openai import OpenAI

def main():
    print("Connecting to local VASUKI OpenAI REST Server (http://localhost:8000/v1)...")
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

    response = client.chat.completions.create(
        model="vasuki-phase7",
        messages=[
            {"role": "system", "content": "You are an expert Python specialist."},
            {"role": "user", "content": "Write quicksort in Python with custom comparator"}
        ],
        stream=True
    )

    print("\nStreamed Response:\n")
    for chunk in response:
        print(chunk.choices[0].delta.content or "", end="", flush=True)
    print()

if __name__ == "__main__":
    main()
