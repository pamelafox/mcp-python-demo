from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


# Optional: create a sampling callback
async def handle_sampling_message(
    context,
    params: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            # Initialize the connection
            await session.initialize()
            tools = await session.list_tools()
            print("Tools:", tools)
            # List prompts
            prompts = await session.list_prompts()
            print("Prompts:", prompts)

            # Test the add_list_of_numbers tool
            result = await session.call_tool("add_list_of_numbers", arguments={"numbers": [1, 2, 3, 4, 5]})
            if result.content and len(result.content) > 0:
                content = result.content[0]
                if content.type == "text":
                    print("Add numbers result:", content.text)

            # Test the count_letter_in_text tool
            result = await session.call_tool("count_letter_in_text", arguments={"text": "Hello World", "letter": "l"})
            if result.content and len(result.content) > 0:
                content = result.content[0]
                if content.type == "text":
                    print("Count letter result:", content.text)

            # Test the Azure CLI tool (this will likely fail since Azure CLI may not be installed)
            result = await session.call_tool("run_azure_cli_command", arguments={"command": "version"})
            if result.content and len(result.content) > 0:
                content = result.content[0]
                if content.type == "text":
                    print("Azure CLI result:", content.text)

            # Test a prompt
            result = await session.get_prompt(
                "explain_code", arguments={"code": "def hello():\n    print('Hello World')", "level": "beginner"}
            )
            if result.messages and len(result.messages) > 0:
                message = result.messages[0]
                if message.content.type == "text":
                    print("Explain code prompt:", message.content.text)

            # Test the debug_help prompt
            result = await session.get_prompt(
                "debug_help", arguments={"error_message": "NameError: name 'x' is not defined", "code": "print(x)"}
            )
            if result.messages and len(result.messages) > 0:
                message = result.messages[0]
                if message.content.type == "text":
                    print("Debug help prompt:", message.content.text)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
