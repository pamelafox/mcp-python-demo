import subprocess

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("My App")


@mcp.prompt()
def explain_code(code: str, level: str = "beginner") -> str:
    """Explain code at different levels of detail"""
    levels = {
        "beginner": "Please explain this code in simple terms for someone new to programming",
        "intermediate": "Please explain this code with moderate technical detail",
        "advanced": "Please provide a detailed technical analysis of this code",
    }
    explanation_request = levels[level]
    return f"{explanation_request}:\n\n```python\n{code}\n```"


@mcp.prompt()
def debug_help(error_message: str, code: str = "") -> str:
    """Get help debugging an error"""
    prompt = f"Help me debug this error: {error_message}"
    if code:
        prompt += f"\n\nRelated code:\n```python\n{code}\n```"
    prompt += "\n\nPlease explain what might be causing this error and suggest solutions."
    return prompt


@mcp.tool(
    description="Add a list of numbers and return structured result with metadata",
    annotations=ToolAnnotations(title="Number Addition Tool", idempotentHint=True, readOnlyHint=True),
)
def add_list_of_numbers(numbers: list[int]) -> dict:
    """Add a list of numbers and return structured result"""
    total = sum(numbers)
    return {
        "numbers": numbers,
        "sum": total,
        "count": len(numbers),
        "average": total / len(numbers) if numbers else 0,
        "min": min(numbers) if numbers else None,
        "max": max(numbers) if numbers else None,
        "summary": f"Sum of {numbers} = {total}",
    }


@mcp.tool(
    description="Count occurrences of a letter in text with detailed analysis",
    annotations=ToolAnnotations(title="Letter Counter Tool", idempotentHint=True, readOnlyHint=True),
)
def count_letter_in_text(text: str, letter: str) -> dict:
    """Count occurrences of a letter in a text with structured output"""
    count = text.count(letter)
    text_length = len(text)
    percentage = (count / text_length * 100) if text_length > 0 else 0

    return {
        "letter": letter,
        "count": count,
        "text_length": text_length,
        "percentage": round(percentage, 1),
        "summary": (
            f"Letter '{letter}' appears {count} times in the text " f"(length: {text_length} chars, {percentage:.1f}%)"
        ),
    }


@mcp.tool(
    description="Run an Azure CLI command with structured output and error handling",
    annotations=ToolAnnotations(
        title="Azure CLI Command Runner", destructiveHint=True, idempotentHint=False, readOnlyHint=False
    ),
)
async def run_azure_cli_command(command: str) -> dict:
    """Run an Azure CLI command with enhanced error handling and structured output"""
    # if command starts with "az", remove it
    if command.startswith("az "):
        command = command[3:]

    try:
        result = subprocess.run(["az"] + command.split(), capture_output=True, text=True, check=True)

        return {
            "success": True,
            "command": f"az {command}",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr if result.stderr else None,
            "message": "Command executed successfully",
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "command": f"az {command}",
            "exit_code": e.returncode,
            "stdout": e.stdout if e.stdout else None,
            "stderr": e.stderr,
            "message": f"Command failed with exit code {e.returncode}",
            "error_type": "CalledProcessError",
        }
    except Exception as e:
        return {
            "success": False,
            "command": f"az {command}",
            "exit_code": None,
            "stdout": None,
            "stderr": None,
            "message": f"Unexpected error: {str(e)}",
            "error_type": type(e).__name__,
        }


if __name__ == "__main__":
    mcp.run()
