# tests/test_security.py
def test_admin_access_control(client, auth_token):
    # Regular user should not access admin endpoint
    response = client.get(
        "/admin",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403

def test_sql_injection_protection(client):
    malicious_search = {"location": "' OR 1=1;--"}
    response = client.post("/jobs/search", json=malicious_search)
    assert response.status_code == 400