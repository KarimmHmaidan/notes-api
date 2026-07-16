def test_create_note(client, auth_headers):
    response = client.post("/notes", json={"title": "Test", "content": "Body"}, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Test"


def test_get_notes_empty(client, auth_headers):
    response = client.get("/notes", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 0


def test_get_note_not_found(client, auth_headers):
    response = client.get("/notes/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_note(client, auth_headers):
    create = client.post("/notes", json={"title": "Old", "content": "Old body"}, headers=auth_headers)
    note_id = create.json()["id"]
    response = client.put(f"/notes/{note_id}", json={"title": "New", "content": "New body"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New"


def test_delete_note(client, auth_headers):
    create = client.post("/notes", json={"title": "Delete me", "content": "..."}, headers=auth_headers)
    note_id = create.json()["id"]
    response = client.delete(f"/notes/{note_id}", headers=auth_headers)
    assert response.status_code == 200


def test_delete_note_not_found(client, auth_headers):
    response = client.delete("/notes/9999", headers=auth_headers)
    assert response.status_code == 404


def test_cannot_access_other_users_notes(client):
    client.post("/register", json={"username": "usera", "email": "a@example.com", "password": "password123"})
    login_a = client.post("/login", data={"username": "usera", "password": "password123"})
    headers_a = {"Authorization": f"Bearer {login_a.json()['access_token']}"}
    note = client.post("/notes", json={"title": "Private", "content": "secret"}, headers=headers_a)
    note_id = note.json()["id"]

    client.post("/register", json={"username": "userb", "email": "b@example.com", "password": "password123"})
    login_b = client.post("/login", data={"username": "userb", "password": "password123"})
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

    response = client.get(f"/notes/{note_id}", headers=headers_b)
    assert response.status_code == 404


def test_pagination(client, auth_headers):
    for i in range(15):
        client.post("/notes", json={"title": f"Note {i}", "content": "..."}, headers=auth_headers)

    response = client.get("/notes?skip=0&limit=10", headers=auth_headers)
    data = response.json()
    assert data["total"] == 15
    assert len(data["items"]) == 10

    response2 = client.get("/notes?skip=10&limit=10", headers=auth_headers)
    assert len(response2.json()["items"]) == 5


def test_sorting_by_title(client, auth_headers):
    client.post("/notes", json={"title": "Zebra", "content": "..."}, headers=auth_headers)
    client.post("/notes", json={"title": "Apple", "content": "..."}, headers=auth_headers)

    response = client.get("/notes?sort_by=title&order=asc", headers=auth_headers)
    titles = [item["title"] for item in response.json()["items"]]
    assert titles == sorted(titles)