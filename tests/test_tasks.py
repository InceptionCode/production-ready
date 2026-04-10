async def test_create_task(client):
    r = await client.post("/api/tasks/", json={"title": "Buy milk"})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


async def test_list_tasks(client):
    await client.post("/api/tasks/", json={"title": "Task 1"})
    await client.post("/api/tasks/", json={"title": "Task 2"})
    r = await client.get("/api/tasks/")
    assert r.status_code == 200
    assert len(r.json()) == 2


async def test_update_task_completed(client):
    created = (await client.post("/api/tasks/", json={"title": "Old title"})).json()
    r = await client.patch(f"/api/tasks/{created['id']}", json={"completed": True})
    assert r.status_code == 200
    data = r.json()
    assert data["completed"] is True
    assert data["title"] == "Old title"  # title unchanged


async def test_update_task_title(client):
    created = (await client.post("/api/tasks/", json={"title": "Old"})).json()
    r = await client.patch(f"/api/tasks/{created['id']}", json={"title": "New"})
    assert r.status_code == 200
    assert r.json()["title"] == "New"
    assert r.json()["completed"] is False  # unchanged


async def test_delete_task(client):
    created = (await client.post("/api/tasks/", json={"title": "Temp"})).json()
    r = await client.delete(f"/api/tasks/{created['id']}")
    assert r.status_code == 204

    # Deleted task is gone
    r2 = await client.delete(f"/api/tasks/{created['id']}")
    assert r2.status_code == 404


async def test_deleted_task_not_in_list(client):
    created = (await client.post("/api/tasks/", json={"title": "Gone"})).json()
    await client.delete(f"/api/tasks/{created['id']}")
    r = await client.get("/api/tasks/")
    assert all(t["id"] != created["id"] for t in r.json())


async def test_create_task_empty_title(client):
    r = await client.post("/api/tasks/", json={"title": ""})
    assert r.status_code == 422


async def test_create_task_missing_title(client):
    r = await client.post("/api/tasks/", json={})
    assert r.status_code == 422


async def test_update_nonexistent_task(client):
    r = await client.patch("/api/tasks/does-not-exist", json={"completed": True})
    assert r.status_code == 404


async def test_delete_nonexistent_task(client):
    r = await client.delete("/api/tasks/does-not-exist")
    assert r.status_code == 404
