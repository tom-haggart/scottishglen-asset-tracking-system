# measure_performance.py
# TEST TOOLING for NFR 3 and 4 (#10) and the unique-ID check (#9). Run with the seeded data in place.
import time
from database import get_assets
from database import count_assets

start = time.perf_counter()
assets = get_assets()
elapsed = time.perf_counter() - start
print(f"get_assets returned {len(assets)} assets in {elapsed:.2f} s")

ids = [asset.asset_id for asset in assets]
print("All IDs unique:", len(set(ids)) == len(ids))

start = time.perf_counter()
page = get_assets(limit=50, offset=0)
total = count_assets()
elapsed = time.perf_counter() - start
print(f"One page of {len(page)} assets plus the count ({total}) in {elapsed:.2f} s")