# self_consistency.py

from collections import Counter
from config import client, MODEL


QUESTION = """
A hotel costs ₹2,000 per night for 3 nights.
Transport costs ₹1,500.
Food costs ₹500 per day for 4 days.
Activities cost ₹1,000.

What is the total trip cost?
"""


PROMPT = """
You are a travel planning assistant.

Solve the problem step by step.
At the end, write:

Final Answer: ₹<amount>
"""


def extract_answer(text):

    for line in reversed(text.splitlines()):

        if "final answer" in line.lower():

            return line.split(":", 1)[-1].strip()

    return text.splitlines()[-1].strip()


def run_many(runs=5):

    answers = []

    for i in range(1, runs + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": PROMPT
                },
                {
                    "role": "user",
                    "content": QUESTION
                }
            ],
            temperature=0.8
        )

        answer = extract_answer(
            response.choices[0].message.content
        )

        print(f"Run {i}: {answer}")

        answers.append(answer)

    return answers


if __name__ == "__main__":

    print("=" * 60)
    print("SELF-CONSISTENCY")
    print("=" * 60)

    print("\nQUESTION:")
    print(QUESTION)

    answers = run_many()

    winner, count = Counter(answers).most_common(1)[0]

    print("\n" + "=" * 60)
    print(f"MAJORITY ANSWER: {winner}")
    print(f"COUNT: {count}/{len(answers)}")
    print("=" * 60)