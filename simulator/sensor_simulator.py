"""
Script giả lập 1,000 thiết bị cảm biến IoT.
Gửi dữ liệu JSON liên tục tới Backend API qua HTTP POST.
"""

import asyncio
import random
import time
from datetime import datetime, timezone

import aiohttp

from config import (
    API_URL,
    DEVICE_COUNT,
    SEND_INTERVAL,
    TEMPERATURE_RANGE,
    HUMIDITY_RANGE,
    CO2_RANGE,
    ANOMALY_PROBABILITY,
)


def generate_reading(device_id: str) -> dict:
    """Tạo một bản ghi cảm biến ngẫu nhiên."""
    # Xác suất nhỏ tạo giá trị bất thường
    if random.random() < ANOMALY_PROBABILITY:
        return {
            "device_id": device_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperature": random.choice([random.uniform(100, 200), random.uniform(-50, -10)]),
            "humidity": random.choice([random.uniform(-20, -1), random.uniform(100, 120)]),
            "co2": random.choice([random.uniform(-100, -1), random.uniform(5000, 10000)]),
        }

    return {
        "device_id": device_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": round(random.uniform(*TEMPERATURE_RANGE), 2),
        "humidity": round(random.uniform(*HUMIDITY_RANGE), 2),
        "co2": round(random.uniform(*CO2_RANGE), 2),
    }


async def send_reading(session: aiohttp.ClientSession, reading: dict):
    """Gửi một bản ghi tới Backend API."""
    try:
        async with session.post(API_URL, json=reading) as resp:
            if resp.status != 200:
                print(f"⚠️ Device {reading['device_id']}: HTTP {resp.status}")
    except Exception as e:
        print(f"❌ Device {reading['device_id']}: {e}")


async def simulate_batch():
    """Gửi dữ liệu từ tất cả thiết bị trong một batch."""
    device_ids = [f"sensor_{i:04d}" for i in range(1, DEVICE_COUNT + 1)]

    async with aiohttp.ClientSession() as session:
        batch_count = 0
        while True:
            batch_count += 1
            start = time.perf_counter()

            # Tạo và gửi dữ liệu song song cho tất cả thiết bị
            tasks = []
            for device_id in device_ids:
                reading = generate_reading(device_id)
                tasks.append(send_reading(session, reading))

            await asyncio.gather(*tasks)

            elapsed = time.perf_counter() - start
            print(
                f"📡 Batch #{batch_count}: Sent {DEVICE_COUNT} readings in {elapsed:.2f}s"
            )

            # Chờ interval trước khi gửi batch tiếp theo
            if elapsed < SEND_INTERVAL:
                await asyncio.sleep(SEND_INTERVAL - elapsed)


if __name__ == "__main__":
    print(f"🚀 Starting IoT Simulator: {DEVICE_COUNT} devices")
    print(f"📡 Target API: {API_URL}")
    print(f"⏱️  Interval: {SEND_INTERVAL}s")
    print("-" * 50)
    asyncio.run(simulate_batch())
