# Day 3 Lab Analysis
## Hospital Appointment and Billing Assistant Using a ReAct Agent

## 1. Problem Statement

The goal of this project is to build a ReAct-based hospital billing assistant.

The agent can read hospital information from an HTML document and perform
mathematical calculations using tools.

The agent uses two tools:

1. `read_hospital_data()` - reads hospital information.
2. `calculator()` - performs mathematical calculations.

The agent follows the ReAct cycle:

Reason → Act → Observe → Reason → Final Answer


## 2. Scenario

The scenario is a hospital appointment and billing assistant.

The hospital information is stored in `hospital.html`.

Example information includes:

- General Medicine consultation: ₹500
- Cardiology consultation: ₹800
- Laboratory test: ₹500
- Registration charge: ₹200
- Senior citizen discount: 10%
- Follow-up consultation: ₹300

For example, if a patient needs:

- Cardiology consultation = ₹800
- Laboratory test = ₹500
- Registration = ₹200

The original total is:

800 + 500 + 200 = ₹1500

After a 10% senior citizen discount:

1500 × 0.9 = ₹1350

The calculator tool is used for this calculation.


## 3. Tools Used

### Tool 1: read_hospital_data()

This tool reads the hospital HTML file.

Example:

read_hospital_data("Day_3Task/hospital.html")

The tool removes HTML tags and returns readable text.

It can also return an error as text if the file does not exist.


### Tool 2: calculator()

This tool evaluates mathematical expressions.

Example:

calculator("(800 + 500 + 200) * 0.9")

Result:

1350


## 4. ReAct Agent Flow

The agent follows these steps:

1. The user provides a question.
2. The LLM understands the question.
3. The LLM decides whether a tool is required.
4. The appropriate tool is called.
5. The tool returns an observation.
6. The LLM uses the observation to continue reasoning.
7. Another tool may be called if necessary.
8. The agent produces the final answer.

Example:

User:
Calculate the hospital cost after the senior citizen discount.

↓

Agent calls:

read_hospital_data()

↓

Hospital information is returned.

↓

Agent calls:

calculator("(800 + 500 + 200) * 0.9")

↓

Calculator returns:

1350

↓

Final answer:

The total cost is ₹1350.


## 5. Failure Mode 1: Missing File

To deliberately create a failure, the agent was asked to read:

missing_patient.html

The file does not exist.

Instead of crashing the program, the tool returns:

"Read error: ... no such file exists"

This demonstrates error-as-text.

The error becomes an observation that the agent can process.


## 6. Failure Mode 2: Repeated Tool Calls

When a file is missing, an agent may repeatedly request the same file.

For example:

read_hospital_data("missing_patient.html")

The same call may be generated again.

This can create an unnecessary loop.

To solve this problem, the fixed agent stores previous tool calls in:

seen_calls

If the same tool call is detected again, the agent does not execute it again.


## 7. Failure Mode 3: Large Tool Output

A large HTML document can produce a very large tool response.

Large observations can increase the amount of context sent to the LLM.

This can make the agent slower and increase resource usage.

To prevent this, the fixed agent limits tool output using:

MAX_TOOL_CHARS = 1500

If the observation is larger than this limit, it is truncated.


## 8. Character Budget Guard

The fixed agent also keeps track of the total amount of tool output.

The limit is:

CHAR_BUDGET = 30000

If the total character count becomes too large, the agent stops.

This prevents uncontrolled growth of the conversation context.


## 9. Unknown Tool Guard

The agent uses a tool registry:

TOOL_FUNCTIONS

When the LLM requests a tool, the program checks whether the tool exists.

If the tool does not exist, the agent returns:

"Unknown tool: tool_name"

instead of crashing.


## 10. Maximum Step Guard

The agent has a maximum number of reasoning/tool steps:

MAX_STEPS = 8

If the agent does not reach a final answer within this limit,
the agent stops.

This prevents an infinite ReAct loop.


## 11. Comparison

| Feature | Basic Agent | Fixed Agent |
|---|---|---|
| Tool calling | Yes | Yes |
| Calculator | Yes | Yes |
| Hospital data reader | Yes | Yes |
| Error-as-text | Yes | Yes |
| Repeated-call protection | No | Yes |
| Output truncation | No | Yes |
| Character budget | No | Yes |
| Unknown-tool protection | Yes | Yes |
| Maximum steps | Yes | Yes |


## 12. Observations

The normal hospital billing question required both tools.

The document reader was used to obtain the hospital charges.

The calculator was then used to calculate the final amount.

The missing-file test demonstrated that tool errors can be returned
as observations instead of causing the program to crash.

The fixed agent also prevented repeated calls and limited the size
of tool observations.


## 13. Conclusion

This experiment demonstrated how a ReAct agent can combine an LLM
with external tools.

The LLM is responsible for understanding the question and deciding
which tool to use.

The tools provide information and perform calculations.

However, an agent needs safeguards because tool failures, repeated
calls, large outputs, and excessive steps can cause problems.

The fixed version improves reliability by adding repeat detection,
output truncation, character budgeting, unknown-tool handling, and
maximum-step limits.