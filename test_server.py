import asyncio

from mcp import Client

from server import mcp


async def main():
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print([t.name for t in tools.tools])
        result = await client.call_tool("get_repo", {"owner": "anthropics", "repo": "anthropic-sdk-python"})
        print(result)


asyncio.run(main())