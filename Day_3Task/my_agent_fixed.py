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

Use calculator when mathematical calculation
is required.

If a tool returns an error, do not repeatedly
make the exact same tool call.

When you have enough information, give the
final answer.
"""


# =========================
# SAFETY LIMITS
# =========================

MAX_STEPS = 8
MAX_TOOL_CHARS = 1500
CHAR_BUDGET = 30000


def run_agent(question):

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

    # Stores previous tool calls
    seen_calls = set()

    # Tracks total tool output
    total_chars = 0


    # =========================
    # REACT LOOP
    # =========================

    for step in range(MAX_STEPS):

        print(f"\n--- STEP {step + 1} ---")


        # =========================
        # CHARACTER BUDGET GUARD
        # =========================

        if total_chars > CHAR_BUDGET:

            print("Character budget exceeded.")

            return (
                "Agent stopped because "
                "character budget was exceeded."
            )


        # =========================
        # ASK LLM
        # =========================

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=TOOLS,

            tool_choice="auto"
        )

        message = response.choices[0].message


        # =========================
        # FINAL ANSWER
        # =========================

        if not message.tool_calls:

            print("\nFINAL ANSWER:")
            print(message.content)

            return message.content


        messages.append(message)


        # =========================
        # PROCESS TOOL CALLS
        # =========================

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print("TOOL:", tool_name)
            print("ARGS:", arguments)


            # =========================
            # CREATE CALL SIGNATURE
            # =========================

            call_signature = (
                tool_name,
                json.dumps(
                    arguments,
                    sort_keys=True
                )
            )


            # =========================
            # REPEAT CALL GUARD
            # =========================

            if call_signature in seen_calls:

                print(
                    "Repeated tool call detected."
                )

                result = (
                    "This exact tool call was "
                    "already made. Do not repeat it. "
                    "Try another approach."
                )

            else:

                seen_calls.add(
                    call_signature
                )


                # =========================
                # FIND TOOL
                # =========================

                tool_function = (
                    TOOL_FUNCTIONS.get(
                        tool_name
                    )
                )


                # =========================
                # UNKNOWN TOOL GUARD
                # =========================

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


            # =========================
            # OUTPUT TRUNCATION
            # =========================

            if len(result) > MAX_TOOL_CHARS:

                result = (
                    result[:MAX_TOOL_CHARS]
                    + "\n[Observation truncated]"
                )


            print("OBSERVATION:")
            print(result)


            # =========================
            # UPDATE CHARACTER COUNT
            # =========================

            total_chars += len(result)


            # =========================
            # SEND OBSERVATION TO LLM
            # =========================

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            )


    # =========================
    # MAX STEP GUARD
    # =========================

    return (
        "Agent stopped because "
        "maximum steps were reached."
    )


# =========================
# TESTS
# =========================

if __name__ == "__main__":

    print("\n==============================")
    print("TEST 1: NORMAL QUESTION")
    print("==============================")

    run_agent(
        """
        Read Day_3Task/hospital.html.

        Calculate the total cost for a patient
        who needs Cardiology consultation,
        Laboratory test and Registration.

        Then apply the 10% senior citizen discount.
        """
    )


    print("\n==============================")
    print("TEST 2: MISSING FILE")
    print("==============================")

    run_agent(
        """
        Read Day_3Task/missing_patient.html
        and tell me the consultation fee.
        """
    )


    print("\n==============================")
    print("TEST 3: NO TOOL")
    print("==============================")

    run_agent(
        """
        Say hello and explain what you can help me with.
        """
    )