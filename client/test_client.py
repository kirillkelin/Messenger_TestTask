import httpx
import asyncio
import random
import time
import logging
import functools
import faker

from utils_and_const import TOTAL_REQUESTS, NUMBER_COROUTINES, NUMBER_REQUESTS, SERVER_URLS, NAMES

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


async def send_one_request(client: httpx.AsyncClient, message: str, username: str):
    url = random.choice(SERVER_URLS)
    data = {"username": username, "message": message}
    headers = {'Content-Type': 'application/json'}
    await client.post(url, json=data, headers=headers, timeout=60)


async def send_requests():
    fake = faker.Faker()
    async with httpx.AsyncClient() as client:
        await asyncio.gather(
            *[send_one_request(client, fake.text(), random.choice(NAMES)) for _ in range(NUMBER_REQUESTS)]
        )


def time_checking(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        await func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        logger.info(f"Time for {TOTAL_REQUESTS} requests: {total_time}")
        logger.info(f"Time for 1 request: {total_time / TOTAL_REQUESTS}")
        logger.info(f"QPS: {TOTAL_REQUESTS / total_time}")

    return wrapper


@time_checking
async def main():
    tasks = [send_requests() for _ in range(NUMBER_COROUTINES)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
