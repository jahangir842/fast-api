import httpx
import asyncio

async def fetch(client, url):
    print(f"Fetching: {url}")
    resp = await client.get(url)
    print(f"Done: {url}")
    return resp.status_code

async def main():
    urls = [
        "https://api.github.com",
        "https://httpbin.org/get",
        "https://example.com",
    ]
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[fetch(client, u) for u in urls])
        print(results)

asyncio.run(main())
