def test_create_user(client) -> None:
    user_dict = dict(username='tester',
                     full_name='',
                     email='test@testing.com',
                     password='password',
                     disabled=False, )

    resp = client.post(f"api/v1/auth/users?administrator_key=administrator", json=user_dict)
    assert resp.status_code == 200

