import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

MCP_URL = "https://ftec5660.ngrok.app/mcp"

async def main():
    client = MultiServerMCPClient(
        {
            "social_graph": {
                "transport": "http",
                "url": MCP_URL,
                "headers": {"ngrok-skip-browser-warning": "true"},
            }
        }
    )
    # 新版写法：单独打开 social_graph 这个服务的 session
    async with client.session("social_graph") as session:
        tools = await session.get_tools()
        print("=== 全部MCP工具列表 ===")
        for t in tools:
            print(f"工具名称：{t.name}，说明：{t.description}")

        linkedin_tool = [t for t in tools if "linkedin" in t.name.lower()][0]
        li_result = await linkedin_tool.ainvoke({"person_id": 10001})
        print("\n===== Kelly Tsang LinkedIn档案（person_id=10001）=====")
        print(li_result)

        fb_tool = [t for t in tools if "facebook" in t.name.lower()][0]
        fb_result = await fb_tool.ainvoke({"user_id": 10001})
        print("\n===== Kelly Tsang Facebook档案（user_id=10001）=====")
        print(fb_result)

if __name__ == "__main__":
    asyncio.run(main())
