# cot_prompt.py

from config import client, MODEL


QUESTIONS = [

    "A hotel costs ₹2,000 per night for 3 nights and transport costs ₹1,500. "
    "Calculate the total travel cost.",

    "The journey from Chennai to Bengaluru takes 6 hours and "
    "Bengaluru to Mysuru takes 3 hours. What is the total travel time?",

    "A student has a travel budget of ₹10,000. "
    "The hotel costs ₹2,000 per night for 3 nights, "
    "transport costs ₹1,500, food costs ₹500 per day for 4 days, "
    "and activities cost ₹1,000. "
    "Calculate the total cost and how much money remains."
]


COT_PROMPT = """
You are a travel planning assistant.

Solve the problem carefully step by step.
Show the important calculations.
Then provide the final answer.

Do not use external tools.
"""


def ask_cot(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": COT_PROMPT
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
    print("CHAIN-OF-THOUGHT PROMPTING")
    print("=" * 60)

    for i, question in enumerate(QUESTIONS, 1):

        print(f"\nQUESTION {i}")
        print(question)

        answer = ask_cot(question)

        print("\nANSWER:")
        print(answer)