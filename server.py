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
    explanation_request = levels.get(level, levels["beginner"])
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
async def add_list_of_numbers(numbers: list[int]) -> str:
    """Add a list of numbers and return structured result"""
    total = sum(numbers)
    return f"Sum of {numbers} = {total}"


@mcp.tool(
    description="Count occurrences of a letter in text with detailed analysis",
    annotations=ToolAnnotations(title="Letter Counter Tool", idempotentHint=True, readOnlyHint=True),
)
def count_letter_in_text(text: str, letter: str) -> str:
    """Count occurrences of a letter in a text with structured output"""
    count = text.count(letter)
    text_length = len(text)
    percentage = (count / text_length * 100) if text_length > 0 else 0

    return f"Letter '{letter}' appears {count} times in the text " f"(length: {text_length} chars, {percentage:.1f}%)"


@mcp.tool(
    description="Run an Azure CLI command with structured output and error handling",
    annotations=ToolAnnotations(
        title="Azure CLI Command Runner", destructiveHint=True, idempotentHint=False, readOnlyHint=False
    ),
)
async def run_azure_cli_command(command: str) -> str:
    """Run an Azure CLI command with enhanced error handling and structured output"""
    # if command starts with "az", remove it
    if command.startswith("az "):
        command = command[3:]

    try:
        result = subprocess.run(["az"] + command.split(), capture_output=True, text=True, check=True)

        return f"Command executed successfully:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Command failed with exit code {e.returncode}:\n{e.stderr}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


if __name__ == "__main__":
    mcp.run()
