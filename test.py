import asyncio
import json
from pathlib import Path

from hw2 import cv_text, load_env_file, load_mcp_tools


def to_json(raw):
    """MCP tool 返回 [{'type':'text','text':'<JSON>'}]，解析成 dict/list。"""
    if isinstance(raw, list) and raw and isinstance(raw[0], dict) and "text" in raw[0]:
        return json.loads(raw[0]["text"])
    if hasattr(raw, "content"):
        raw = raw.content
        if isinstance(raw, list) and raw and isinstance(raw[0], dict) and "text" in raw[0]:
            return json.loads(raw[0]["text"])
    return raw


async def main():
    load_env_file()
    tools = await load_mcp_tools()
    tmap = {t.name: t for t in tools}

    calls = [
        ("LinkedIn profile 10001", "get_linkedin_profile", {"person_id": 10001}),
        ("Facebook profile 10001", "get_facebook_profile", {"user_id": 10001}),
        ("LinkedIn interactions 10001", "get_linkedin_interactions", {"person_id": 10001}),
        ("Search LinkedIn 'Kelly Tsang'", "search_linkedin_people", {"q": "Kelly Tsang", "limit": 20}),
        ("Search Facebook 'Kel Tsang'", "search_facebook_users", {"q": "Kel Tsang", "limit": 20}),
    ]

    for label, tool_name, args in calls:
        print("=" * 70)
        print(label)
        try:
            raw = await tmap[tool_name].ainvoke(args)
            print(json.dumps(to_json(raw), ensure_ascii=False, indent=2))
        except Exception as exc:
            print("ERROR:", repr(exc))

    target = Path("task2/target_cv.pdf")
    if target.is_file():
        print("=" * 70)
        print("task2/target_cv.pdf text")
        print(cv_text(target))


if __name__ == "__main__":
    asyncio.run(main())
