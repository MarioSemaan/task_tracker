# app/verify_b.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def expect_status(label, response, expected):
    if response.status_code == expected:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label} — expected {expected}, got {response.status_code} ({response.text})")


# 1. Valid task created
r = client.post("/tasks", json={"title": "Write tests"})
expect_status("valid task -> 201", r, 201)
if r.status_code == 201:
    body = r.json()
    assert "id" in body, "FAIL: response missing id"
    print("PASS: response includes id")

# 2. Missing title
r = client.post("/tasks", json={})
expect_status("missing title -> 422", r, 422)

# 3. Blank title
r = client.post("/tasks", json={"title": "   "})
expect_status("blank title -> 422", r, 422)

# 4. Overlong title
r = client.post("/tasks", json={"title": "x" * 201})
expect_status("overlong title -> 422", r, 422)

# 5. Invalid status
r = client.post("/tasks", json={"title": "x", "status": "Whatever"})
expect_status("invalid status -> 422", r, 422)

# 6. Invalid priority
r = client.post("/tasks", json={"title": "x", "priority": "Whatever"})
expect_status("invalid priority -> 422", r, 422)

# 7. Unknown field
r = client.post("/tasks", json={"title": "x", "made_up": "value"})
expect_status("unknown field -> 422", r, 422)

print("--- Part B verifications complete ---")