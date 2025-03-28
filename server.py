import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"

@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"

@mcp.tool()
async def add_list_of_numbers(numbers: list[int]) -> int:
    """Add a list of numbers"""
    return sum(numbers)

@mcp.tool()
def count_letter_in_text(text: str, letter: str) -> int:
    """Count occurrences of a letter in a text"""
    return text.count(letter)

@mcp.tool()
async def run_azure_cli_command(command: str) -> str:
    """Run an Azure CLI command"""
    # if command starts with "az", remove it
    if command.startswith("az "):
        command = command[3:]
    result = subprocess.run(
        ["az"] + command.split(),
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

if __name__ == "__main__":
    mcp.run()