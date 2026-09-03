import asyncio
import random
import time

import httpx

API_URL = "http://localhost:8000"

async def fetch(client, endpoint):
    try:
        response = await client.get(f"{API_URL}{endpoint}")
        return response.status_code
    except Exception:  # noqa: BLE001
        return 500

async def traffic_generator():
    endpoints = [
        "/api/v1/regime/current?model_type=hmm",
        "/api/v1/regime/current?model_type=lstm",  # Hit PyTorch model
        "/health/live",
        "/health/ready",
        "/api/v1/invalid_endpoint" # generates 404s
    ]
    
    print("Starting MacroRegime API Stress Test...")
    print("Simulating base traffic, flash crashes, and malicious requests.")
    
    async with httpx.AsyncClient() as client:
        while True:
            # Randomize traffic intensity (10 to 100 req/s)
            is_flash_crash = random.random() > 0.85
            reqs_per_sec = random.randint(50, 150) if is_flash_crash else random.randint(5, 20)
            
            if is_flash_crash:
                print(f"[{time.strftime('%X')}] FLASH CRASH DETECTED! Spiking traffic to {reqs_per_sec} RPS...")
            else:
                print(f"[{time.strftime('%X')}] Normal traffic: {reqs_per_sec} RPS...")

            tasks = []
            for _ in range(reqs_per_sec):
                endpoint = random.choice(endpoints)
                tasks.append(fetch(client, endpoint))
            
            # Execute burst
            results = await asyncio.gather(*tasks)
            
            # Print brief summary
            status_counts = {}
            for r in results:
                status_counts[r] = status_counts.get(r, 0) + 1
            print(f"  -> Results: {status_counts}")
            
            await asyncio.sleep(1.0)

if __name__ == "__main__":
    try:
        asyncio.run(traffic_generator())
    except KeyboardInterrupt:
        print("\nStress test stopped.")
