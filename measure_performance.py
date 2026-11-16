# measure_performance.py
# TEST TOOLING for NFR 3 and 4 (#10) and the unique-ID check (#9). Run with the seeded data in place.
import time
from database import get_assets
from database import count_assets
from database import add_asset, update_asset, delete_asset
from models import HardwareDetails

def time_it(label, function, *arguments):
    """Runs function once with the given arguments and prints how long it took."""
    start = time.perf_counter()
    result = function(*arguments)
    print(f"{label}: {time.perf_counter() - start:.2f} s")
    return result

# Marked SEED, so cleanup_test_data.sql would remove it if the script stopped half way.
hardware = HardwareDetails("SEED-TIMING", "Test model", "Test maker", "Windows", "10.0.0.1")
new_id = time_it("Add asset", add_asset, hardware, 1, None, "SEED")
time_it("Edit asset", update_asset, new_id, 1, "2025-02-02", "SEED")
time_it("Delete asset", delete_asset, new_id)

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