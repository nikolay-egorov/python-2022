import asyncio
import os
import sys

import aiohttp as aiohttp


async def download_job(download_number: int, p: str, from_url: str):
    params = {
        "https://picsum.photos": 600
    }

    def file_open(num: int):
        return open(f"{p}/{num}.png", "bw")

    async with aiohttp.ClientSession() as session:
        full_url = f"{from_url}/{params.get(from_url, '')}"
        for i in range(1, download_number + 1):
            with file_open(i) as f:
                async with session.get(full_url) as ans:
                    f.write((await ans.content.read()))


def download_results(download_num: int, dest: str, from_url: str = "https://picsum.photos"):
    os.makedirs(f"{dest}", exist_ok=True)
    asyncio.get_event_loop().run_until_complete(download_job(download_num, dest, from_url))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        total_num = int(sys.argv[1])
    else:
        total_num = 7
    download_results(total_num, "artifacts/simple")
