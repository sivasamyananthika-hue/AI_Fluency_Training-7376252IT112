import ast
import operator
import os
import re
import requests


# =========================
# CALCULATOR TOOL
# =========================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_eval(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):

        left = safe_eval(node.left)
        right = safe_eval(node.right)

        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError(
                "Use only + - * / ( )."
            )

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):

        value = safe_eval(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return value

    raise ValueError(
        "Use only numbers and + - * / ( )."
    )


def calculator(expression):

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = safe_eval(tree.body)

        return str(result)

    except Exception as e:

        return f"Calculator error: {e}"


# =========================
# HOSPITAL DATA READER
# =========================

def read_hospital_data(path):

    try:

        if os.path.exists(path):

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

        elif (
            path.startswith("http://")
            or path.startswith("https://")
        ):

            response = requests.get(
                path,
                timeout=10
            )

            response.raise_for_status()

            text = response.text

        else:

            return (
                f"Read error: '{path}' "
                "is not a URL and no such file exists"
            )

        # Remove script
        text = re.sub(
            r"<script.*?</script>",
            "",
            text,
            flags=re.S
        )

        # Remove HTML tags
        text = re.sub(
            r"<[^>]+>",
            " ",
            text
        )

        # Remove extra spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        # Limit output
        text = text[:2000]

        return text

    except Exception as e:

        return f"Read error: {e}"


# =========================
# TOOL REGISTRY
# =========================

TOOL_FUNCTIONS = {
    "calculator": calculator,
    "read_hospital_data": read_hospital_data
}


# =========================
# TOOL SCHEMAS
# =========================

TOOLS = [

    {
        "type": "function",

        "function": {

            "name": "calculator",

            "description":
                "Calculate a mathematical expression.",

            "parameters": {

                "type": "object",

                "properties": {

                    "expression": {
                        "type": "string"
                    }

                },

                "required": [
                    "expression"
                ]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name":
                "read_hospital_data",

            "description":
                "Read hospital information from a local HTML file or webpage.",

            "parameters": {

                "type": "object",

                "properties": {

                    "path": {
                        "type": "string"
                    }

                },

                "required": [
                    "path"
                ]
            }
        }
    }
]


# =========================
# TEST TOOLS
# =========================

if __name__ == "__main__":

    print(
        calculator(
            "800 + 500 + 200"
        )
    )

    print(
        calculator(
            "(800 + 500 + 200) * 0.9"
        )
    )

    print(
        read_hospital_data(
            "Day_3Task/hospital.html"
        )
    )

    print(
        read_hospital_data(
            "Day_3Task/missing_patient.html"
        )
    )