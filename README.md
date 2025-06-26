# MCP Python Demo

This repository demonstrates the use of Model Context Protocol (MCP) SDK for Python.

## Setup

### If using Dev Container (Recommended)

If you're using the dev container (VS Code with Docker), everything is already set up for you! The container includes Python, uv, and all necessary tools.

### If running locally

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already

2. Install dependencies from pyproject.toml:
   ```sh
   uv sync --dev
   ```

## Running Development Inspector

To run the development inspector:

```sh
mcp dev server.py
```

## Installing in Claude

To install this MCP plugin in Claude:

1. Run this command:

   ```sh
   mcp install server.py
   ```

2. Restart Claude

3. Troubleshooting: If you get an error, fix the uv path in the config to an absolute path:

   ```sh
   which uv
   ```

   Then update the configuration with the absolute path.

## Installing in GitHub Copilot

📺 If you prefer learning from videos, watch [this video from Burke Holland](https://www.youtube.com/watch?v=Wp0p7iKH6ho) or [this video from James Montemagno](https://www.youtube.com/watch?v=iS25RFups4A).

### If you already installed in Claude Desktop

Enable `chat.mcp.discovery.enabled: true` in your settings and VS Code will discover existing MCP server lists, and proceed to [use the tool in GitHub Copilot Agent mode](#using-tools-in-copilot).

### If you did not install in Claude Desktop

* If you want to associate the MCP server only with a particular repo, create a `.vscode/mcp.json` file with this content:

   ```json
   {
   "inputs": [
   ],
   "servers": {
         "pamelas-mcp": {
            "command": "PATH/TO/uv",
            "args": [
               "--directory",
               "/PATH/TO/mcp-python-demo",
               "run",
               "server.py"
            ]
         }
   }
   }
   ```

* Alternatively, if you want to associate the MCP server with all repos, add to your VS Code User Settings JSON:

   ```json
   {
   "mcp": {
      "inputs": [],
      "servers": {
         "pamelas-mcp": {
         "command": "/PATH/TO/uv",
         "args": [
            "--directory",
            "/PATH/TO/mcp-python-demo",
            "run",
            "server.py"
         ]
         }
      }
   }
   }
   ```

   Another way to update settings is to run this command in the terminal:

   ```bash
   code-insiders --add-mcp "{\"name\":\"pamelas-mcp\",\"command\":\"/PATH/TO/uv\",\"args\":[\"--directory\",\"/PATH/TO/mcp-python-demo\",\"run\",\"server.py\"]}"
   ```

## Using tools in Copilot

1. Now that the mcp server is discoverable, open GitHub Copilot and select the `Agent` mode (not `Chat` or `Edits`).
2. Select the "refresh" button in the top right corner of the Copilot chat text field to refresh the server list.
3. Select the "🛠️" button to see all the possible tools, including the ones from this repo.
4. Put a question in the chat that would naturally invoke one of the tools, for example: "What is the current weather in Seattle?".
