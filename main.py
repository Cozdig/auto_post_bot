import asyncio

from src.scheduler import PostScheduler


async def main():
    test_scheduler = PostScheduler()
    await test_scheduler.run()

if __name__ == "__main__":
    asyncio.run(main())