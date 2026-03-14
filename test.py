import requests
import json

BASE_URL = "http://localhost:5000"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

token = None
created_ids = {}

def log(method, endpoint, status, ok, note=""):
    icon = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
    print(f"  [{icon}] {method:<6} {endpoint:<40} {status}  {note}")

def test(method, endpoint, payload=None, auth=True, label=None):
    url = BASE_URL + endpoint
    headers = {"Content-Type": "application/json"}
    if auth and token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = getattr(requests, method)(url, json=payload, headers=headers, timeout=5)
        ok = resp.status_code < 400
        note = ""
        try:
            data = resp.json()
            if not ok:
                note = str(data)[:60]
        except:
            data = {}
        log(method.upper(), endpoint, resp.status_code, ok, note)
        return resp, data
    except requests.exceptions.ConnectionError:
        print(f"  [{RED}ERR {RESET}] Cannot connect to {BASE_URL} — is Flask running?")
        return None, {}
    except Exception as e:
        print(f"  [{RED}ERR {RESET}] {endpoint} — {e}")
        return None, {}


print(f"\n{BOLD}CoreInventory Backend Test{RESET}")
print("=" * 60)

# ── Home ──────────────────────────────────────────────────────
print(f"\n{BOLD}[Home]{RESET}")
test("get", "/", auth=False)

# ── Auth ──────────────────────────────────────────────────────
print(f"\n{BOLD}[Auth]{RESET}")

resp, data = test("post", "/auth/register", {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "Test@1234"
}, auth=False)

resp, data = test("post", "/auth/login", {
    "email": "testuser@example.com",
    "password": "Test@1234"
}, auth=False)

if resp and resp.status_code == 200:
    token = data.get("token") or data.get("access_token") or data.get("data", {}).get("token")
    if token:
        print(f"  {YELLOW}Token acquired{RESET}")
    else:
        print(f"  {YELLOW}Warning: logged in but no token found in response — auth headers won't be sent{RESET}")

# ── Products ──────────────────────────────────────────────────
print(f"\n{BOLD}[Products]{RESET}")

resp, data = test("post", "/products", {
    "name": "Test Widget",
    "sku": "SKU-001",
    "quantity": 100,
    "price": 9.99,
    "category": "General"
})
if resp and resp.status_code in (200, 201):
    pid = data.get("id") or data.get("data", {}).get("id")
    if pid:
        created_ids["product"] = pid

test("get", "/products")

if "product" in created_ids:
    pid = created_ids["product"]
    test("get", f"/products/{pid}")
    test("put", f"/products/{pid}", {"name": "Updated Widget", "quantity": 150})
else:
    print(f"  {YELLOW}Skipping GET/PUT by ID — product creation failed{RESET}")

# ── Receipts ──────────────────────────────────────────────────
print(f"\n{BOLD}[Receipts]{RESET}")

resp, data = test("post", "/receipts", {
    "product_id": created_ids.get("product", 1),
    "quantity": 50,
    "notes": "Test receipt"
})
if resp and resp.status_code in (200, 201):
    rid = data.get("id") or data.get("data", {}).get("id")
    if rid:
        created_ids["receipt"] = rid

test("get", "/receipts")
if "receipt" in created_ids:
    test("get", f"/receipts/{created_ids['receipt']}")

# ── Deliveries ────────────────────────────────────────────────
print(f"\n{BOLD}[Deliveries]{RESET}")

resp, data = test("post", "/deliveries", {
    "product_id": created_ids.get("product", 1),
    "quantity": 10,
    "notes": "Test delivery"
})
if resp and resp.status_code in (200, 201):
    did = data.get("id") or data.get("data", {}).get("id")
    if did:
        created_ids["delivery"] = did

test("get", "/deliveries")
if "delivery" in created_ids:
    test("get", f"/deliveries/{created_ids['delivery']}")

# ── Transfers ─────────────────────────────────────────────────
print(f"\n{BOLD}[Transfers]{RESET}")

resp, data = test("post", "/transfers", {
    "product_id": created_ids.get("product", 1),
    "quantity": 5,
    "from_location": "Warehouse A",
    "to_location": "Warehouse B",
    "notes": "Test transfer"
})
if resp and resp.status_code in (200, 201):
    tid = data.get("id") or data.get("data", {}).get("id")
    if tid:
        created_ids["transfer"] = tid

test("get", "/transfers")
if "transfer" in created_ids:
    test("get", f"/transfers/{created_ids['transfer']}")

# ── Adjustments ───────────────────────────────────────────────
print(f"\n{BOLD}[Adjustments]{RESET}")

resp, data = test("post", "/adjustments", {
    "product_id": created_ids.get("product", 1),
    "quantity": -5,
    "reason": "Damaged goods",
    "notes": "Test adjustment"
})
if resp and resp.status_code in (200, 201):
    aid = data.get("id") or data.get("data", {}).get("id")
    if aid:
        created_ids["adjustment"] = aid

test("get", "/adjustments")
if "adjustment" in created_ids:
    test("get", f"/adjustments/{created_ids['adjustment']}")

# ── Dashboard ─────────────────────────────────────────────────
print(f"\n{BOLD}[Dashboard]{RESET}")
test("get", "/dashboard")

# ── Move History ──────────────────────────────────────────────
print(f"\n{BOLD}[Move History]{RESET}")
test("get", "/move-history")

# ── Summary ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print(f"{BOLD}Done.{RESET} Fix any FAIL routes above and re-run.\n")