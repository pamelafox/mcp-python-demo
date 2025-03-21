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
    message: types.CreateMessageRequestParams,
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
        async with ClientSession(
            read, write, sampling_callback=handle_sampling_message
        ) as session:
            # Initialize the connection
            await session.initialize()
            tools = await session.list_tools()
            print("Tools:", tools)
            # List prompts
            prompts = await session.list_prompts()
            print("Prompts:", prompts)

            # Read a resource
            resource_results = await session.read_resource("config://app")
            print("Resource content:", resource_results.contents[0].text)

            # Call a tool
            result = await session.call_tool("calculate_bmi", arguments={"weight_kg": "5", "height_m": "1.5"})
            print("Tool result:", result.content[0].text)

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())