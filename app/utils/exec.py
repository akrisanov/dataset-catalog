import asyncio
import concurrent.futures


async def run_in_thread_executor(func, *args, **kwargs):
    """Run blocking code in ThreadPoolExecutor for IO-bound tasks."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


async def run_in_process_executor(func, *args, **kwargs):
    """Run blocking code in ProcessPoolExecutor for CPU-bound tasks."""
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, func, *args, **kwargs)
