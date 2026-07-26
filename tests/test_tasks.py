# FILE: tests/test_tasks.py
import pytest

# POST /tasks

def test_create_task_valid_returns_201_with_full_body(client):
    r = client.post("/tasks", json={"title": "My Task"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "My Task"
    assert "id" in body
    assert "created_at" in body
    assert "status" in body
    assert "priority" in body

def test_create_task_missing_title_returns_422(client):
    r = client.post("/tasks", json={})
    assert r.status_code == 422

def test_create_task_blank_title_returns_422(client):
    r = client.post("/tasks", json={"title": ""})
    assert r.status_code == 422

def test_create_task_invalid_priority_returns_422(client):
    r = client.post("/tasks", json={"title": "X", "priority": "INVALID"})
    assert r.status_code == 422

def test_create_task_unknown_field_returns_422(client):
    r = client.post("/tasks", json={"title": "X", "unknown": 123})
    assert r.status_code == 422

# GET /tasks

def test_list_tasks_empty_returns_200_and_empty_list(client):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []

def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client, created_task):
    r = client.get("/tasks", params={"status": "Done"})
    assert r.status_code == 200
    assert r.json() == []

def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "A", "priority": "High"})
    client.post("/tasks", json={"title": "B", "priority": "Low"})
    r = client.get("/tasks", params={"priority": "High"})
    assert r.status_code == 200
    assert all(task["priority"] == "High" for task in r.json())
    assert len(r.json()) == 1

# GET /tasks/{id}

def test_get_task_by_id_returns_task(client, created_task):
    r = client.get(f"/tasks/{created_task['id']}")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == created_task["id"]
    assert body["title"] == created_task["title"]

def test_get_task_by_id_not_found_returns_404_with_detail(client):
    r = client.get("/tasks/doesnotexist")
    assert r.status_code == 404
    assert r.json()["detail"].startswith("Task with id doesnotexist not found")

# PATCH /tasks/{id}

def test_patch_partial_update_keeps_other_fields(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"priority": "High"})
    assert r.status_code == 200
    body = r.json()
    assert body["priority"] == "High"
    assert body["title"] == created_task["title"]

def test_patch_not_found_returns_404(client):
    r = client.patch("/tasks/doesnotexist", json={"priority": "High"})
    assert r.status_code == 404
    assert r.json()["detail"].startswith("Task with id doesnotexist not found")

def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"status": "InProgress"})
    assert r.status_code == 200
    assert r.json()["status"] == "InProgress"

def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"status": "Done"})
    assert r.status_code == 422
    assert "Invalid status transition" in r.json()["detail"]

def test_patch_same_status_returns_422(client, created_task):
    r = client.patch(f"/tasks/{created_task['id']}", json={"status": "ToDo"})
    assert r.status_code == 422
    assert "Invalid status transition" in r.json()["detail"]

def test_patch_empty_json_body_returns_422_validation_error(client):
    # Arrange: create a task to update
    create = client.post("/tasks", json={"title": "Empty Update Task"})
    assert create.status_code == 201
    task = create.json()
    # Act: send an empty JSON body for PATCH
    r = client.patch(f"/tasks/{task['id']}", json={})
    # Assert: API rejects the no-op update with validation error
    assert r.status_code == 422
    body = r.json()
    assert "detail" in body
    assert body["detail"], "Expected validation error detail for empty update"

def test_patch_with_unknown_field_returns_422_validation_error(client):
    # Arrange: create a task to update
    create = client.post("/tasks", json={"title": "Unknown Field Task"})
    assert create.status_code == 201
    task = create.json()
    # Act: send a PATCH with an unknown field
    r = client.patch(f"/tasks/{task['id']}", json={"foo": "bar"})
    # Assert: API rejects the unknown field with validation error
    assert r.status_code == 422
    body = r.json()
    assert "detail" in body
    detail = body["detail"]
    if isinstance(detail, list):
        assert any("foo" in str(d) or "extra" in str(d) or "field" in str(d) for d in detail)
    else:
        assert "foo" in str(detail) or "extra" in str(detail) or "field" in str(detail)

def test_patch_invalid_priority_returns_422_validation_error(client):
    # Arrange: create a task to update
    create = client.post("/tasks", json={"title": "Invalid Priority Task"})
    assert create.status_code == 201
    task = create.json()
    # Act: send a PATCH with an invalid priority value
    r = client.patch(f"/tasks/{task['id']}", json={"priority": "Critical"})
    # Assert: API rejects invalid enum value with validation error
    assert r.status_code == 422
    body = r.json()
    assert "detail" in body
    detail = body["detail"]
    if isinstance(detail, list):
        assert any("priority" in str(d).lower() or "enum" in str(d).lower() for d in detail)
    else:
        assert "priority" in str(detail).lower() or "enum" in str(detail).lower()

# DELETE /tasks/{id}

def test_delete_existing_returns_204_no_body(client, created_task):
    r = client.delete(f"/tasks/{created_task['id']}")
    assert r.status_code == 204
    assert r.content == b""

def test_delete_missing_returns_404(client):
    r = client.delete("/tasks/doesnotexist")
    assert r.status_code == 404
    assert r.json()["detail"].startswith("Task with id doesnotexist not found")