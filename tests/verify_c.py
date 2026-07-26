# app/verify_c.py
from fastapi.testclient import TestClient
from app.main import app
from app import storage

client = TestClient(app)


def expect_status(label, response, expected):
    if response.status_code == expected:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label} — expected {expected}, got {response.status_code} ({response.text})")


def make_task(title="Test task"):
    r = client.post("/tasks", json={"title": title})
    return r.json()["id"]


storage._reset()

# --- GET /tasks/{id} ---
task_id = make_task("Get test")
r = client.get(f"/tasks/{task_id}")
expect_status("GET existing task -> 200", r, 200)

r = client.get("/tasks/nonexistent-id")
expect_status("GET nonexistent task -> 404", r, 404)

# --- PATCH: valid forward transitions ---
task_id = make_task("Forward transitions")
r = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
expect_status("ToDo -> InProgress -> 200", r, 200)

r = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
expect_status("InProgress -> Done -> 200", r, 200)

task_id2 = make_task("Skip transition")
r = client.patch(f"/tasks/{task_id2}", json={"status": "Done"})
expect_status("ToDo -> Done (skip) -> 200", r, 200)

# --- PATCH: same-status no-op ---
task_id3 = make_task("No-op transition")
r = client.patch(f"/tasks/{task_id3}", json={"status": "ToDo"})
expect_status("ToDo -> ToDo (no-op) -> 200", r, 200)

# --- PATCH: invalid backward transitions ---
task_id4 = make_task("Backward from Done")
client.patch(f"/tasks/{task_id4}", json={"status": "InProgress"})
client.patch(f"/tasks/{task_id4}", json={"status": "Done"})
r = client.patch(f"/tasks/{task_id4}", json={"status": "ToDo"})
expect_status("Done -> ToDo -> 422", r, 422)

r = client.patch(f"/tasks/{task_id4}", json={"status": "InProgress"})
expect_status("Done -> InProgress -> 422", r, 422)

task_id5 = make_task("Backward from InProgress")
client.patch(f"/tasks/{task_id5}", json={"status": "InProgress"})
r = client.patch(f"/tasks/{task_id5}", json={"status": "ToDo"})
expect_status("InProgress -> ToDo -> 422", r, 422)

# --- PATCH: nonexistent task ---
r = client.patch("/tasks/nonexistent-id", json={"status": "Done"})
expect_status("PATCH nonexistent task -> 404", r, 404)

# --- DELETE ---
task_id6 = make_task("Delete test")
r = client.delete(f"/tasks/{task_id6}")
expect_status("DELETE existing task -> 204", r, 204)

r = client.get(f"/tasks/{task_id6}")
expect_status("GET deleted task -> 404", r, 404)

r = client.delete("/tasks/nonexistent-id")
expect_status("DELETE nonexistent task -> 404", r, 404)

print("--- Part C verifications complete ---")