# measure_performance.py
# TEST TOOLING for NFR 3 and 4 (#10) and the unique-ID check (#9). Run with the seeded data in place.
import time
from database import get_assets

start = time.perf_counter()
assets = get_assets()
elapsed = time.perf_counter() - start
print(f"get_assets returned {len(assets)} assets in {elapsed:.2f} s")

ids = [asset.asset_id for asset in assets]
print("All IDs unique:", len(set(ids)) == len(ids))
