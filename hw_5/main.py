import asyncio
import os
import sys

import aiofiles
import aiohttp as aiohttp


async def download_job(download_number: int, p: str, from_url: str):
    params = {
        "https://picsum.photos": 600
    }

    async def single_job(it: int, s: aiohttp.ClientSession):
        async with aiofiles.open(f"{p}/{it}.png", "bw") as f:
            async with s.get(full_url) as ans:
                await f.write(await (ans.content.read()))

    jobs = []
    async with aiohttp.ClientSession() as session:
        full_url = f"{from_url}/{params.get(from_url, '')}"
        for i in range(1, download_number + 1):
            jobs.append(single_job(i, session))
        # await asyncio.wait(tasks)
        await asyncio.gather(*jobs)


def download_results(download_num: int, dest: str, from_url: str = "https://picsum.photos"):
    os.makedirs(f"{dest}", exist_ok=True)
    asyncio.get_event_loop().run_until_complete(download_job(download_num, dest, from_url))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        total_num = int(sys.argv[1])
    else:
        total_num = 7
    download_results(total_num, "artifacts/simple")
