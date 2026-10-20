import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    mcp_token = os.environ["MCP_TOKEN"]
    client = MultiServerMCPClient({
        "socialgraph": {
            "transport": "streamable_http",
            "url": "https://ftec5660.ngrok.app/mcp",
            "headers": {"Authorization": f"Bearer {mcp_token}"}
        }
    })
    async with client:
        tools = await client.get_tools()
        for t in tools:
            print(t.name, " | ", t.description)

        linkedin_tool = [t for t in tools if "linkedin" in t.name.lower()][0]
        res_li = await linkedin_tool.ainvoke({"person_id": 10001})
        print("\n=== Kelly LinkedIn ===")
        print(res_li)

        fb_tool = [t for t in tools if "facebook" in t.name.lower()][0]
        res_fb = await fb_tool.ainvoke({"user_id": 10001})
        print("\n=== Kelly Facebook ===")
        print(res_fb)

if __name__ == "__main__":
    asyncio.run(main())

