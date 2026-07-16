def test_register_user(client):
    response = client.post("/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"


def test_register_duplicate_user(client):
    payload = {"username": "dupeuser", "email": "dupe@example.com", "password": "password123"}
    client.post("/register", json=payload)
    response = client.post("/register", json=payload)
    assert response.status_code == 409


def test_login_success(client):
    client.post("/register", json={
        "username": "loginuser", "email": "login@example.com", "password": "password123"
    })
    response = client.post("/login", data={"username": "loginuser", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_wrong_password(client):
    client.post("/register", json={
        "username": "wronguser", "email": "wrong@example.com", "password": "password123"
    })
    response = client.post("/login", data={"username": "wronguser", "password": "wrongpass1"})
    assert response.status_code == 401


def test_logout(client):
    client.post("/register", json={
        "username": "logoutuser", "email": "logout@example.com", "password": "password123"
    })
    login_resp = client.post("/login", data={"username": "logoutuser", "password": "password123"})
    refresh_token = login_resp.json()["refresh_token"]

    response = client.post("/logout", json={"refresh_token": refresh_token})
    assert response.status_code == 200

    # using it again should fail — it's revoked
    refresh_resp = client.post("/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 401 