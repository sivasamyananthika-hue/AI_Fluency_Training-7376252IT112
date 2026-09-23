# direct_prompt.py

from config import client, MODEL

QUESTIONS = [

    "A hotel costs ₹2,000 per night for 3 nights and transport costs ₹1,500. "
    "Calculate the total travel cost.",

    "The journey from Chennai to Bengaluru takes 6 hours and "
    "Bengaluru to Mysuru takes 3 hours. What is the total travel time?",

    "What is the current fare for route CHN-BLR?"
]


def ask_direct(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a travel planning assistant. "
                    "Answer the user's question directly. "
                    "Do not use tools."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    print("=" * 60)
    print("DIRECT PROMPTING")
    print("=" * 60)

    for i, question in enumerate(QUESTIONS, 1):

        print(f"\nQUESTION {i}")
        print(question)

        answer = ask_direct(question)

        print("\nANSWER:")
        print(answer)