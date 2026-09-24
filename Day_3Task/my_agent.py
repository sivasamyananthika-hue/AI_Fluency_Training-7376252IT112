import os
import json

from dotenv import load_dotenv
from groq import Groq

from my_tools import TOOL_FUNCTIONS, TOOLS


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv(
    "MODEL",
    "openai/gpt-oss-120b"
)


SYSTEM_PROMPT = """
You are a hospital billing assistant.

You have two tools:

1. read_hospital_data(path)
2. calculator(expression)

Use read_hospital_data when hospital information
must be obtained from a document.

Use calculator when a mathematical calculation
is required.

When you have enough information, provide the
final answer.
"""


def run_agent(question, max_steps=8):

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": question
        }

    ]

    for step in range(max_steps):

        print(
            f"\n--- STEP {step + 1} ---"
        )

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=TOOLS,

            tool_choice="auto"
        )

        message = response.choices[0].message


        # -------------------------
        # FINAL ANSWER
        # -------------------------

        if not message.tool_calls:

            print("\nFINAL ANSWER:")

            print(message.content)

            return message.content


        messages.append(message)


        # -------------------------
        # TOOL CALL
        # -------------------------

        for tool_call in message.tool_calls:

            tool_name = (
                tool_call.function.name
            )

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(
                "TOOL:",
                tool_name
            )

            print(
                "ARGS:",
                arguments
            )


            # Safe tool lookup
            tool_function = (
                TOOL_FUNCTIONS.get(tool_name)
            )


            if tool_function is None:

                result = (
                    f"Unknown tool: {tool_name}"
                )

            else:

                try:

                    result = tool_function(
                        **arguments
                    )

                except Exception as e:

                    result = (
                        f"Tool error: {e}"
                    )


            print(
                "OBSERVATION:"
            )

            print(result)


            messages.append({

                "role": "tool",

                "tool_call_id":
                    tool_call.id,

                "content": result
            })


    return (
        "Agent stopped because "
        "maximum steps were reached."
    )


# =========================
# TEST
# =========================

if __name__ == "__main__":

    question = """
    Read Day_3Task/missing_patient.html
    and tell me the consultation fee.
    """

    run_agent(question)