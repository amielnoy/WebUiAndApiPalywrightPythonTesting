from api_tests.globals import ApiHttpConstants
from api_tests.posts_service import post_requests


def test_get_posts_count(api_json_placeholder):
    pr=post_requests()
    response = pr.get_all_posts(api_json_placeholder)
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    assert len(data) == 100

def test_get_post_number1(api_json_placeholder):
    pr = post_requests()
    response = pr.get_post_by_number(api_json_placeholder, "1")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    assert data['userId'] == 1,"error in user id,expected 1"
    assert data['id'] == 1,"error is user id,expected 1"
    assert data['title'] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit","eror in title"
    assert data['body'] == "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto","erorr in body"

def test_create_post(api_json_placeholder):
    payload = {
        "userId": 1,
        "title": "New test post",
        "body": "This is a body of the test post"
    }
    pr = post_requests()
    response = pr.create_post(api_json_placeholder, payload)
    assert response.status_code == ApiHttpConstants.CREATED
    data = response.json()
    assert data["title"] == payload["title"],"data <> payload!"

def test_update_post(api_json_placeholder):
    payload = {
        "id": 1,
        "title": "Updated title",
        "body": "Updated body",
        "userId": 1
    }
    pr = post_requests()
    response = pr.update_post(api_json_placeholder, payload)
    assert response.status_code == ApiHttpConstants.OK
    assert response.json()["title"] == "Updated title"

def test_delete_post_by_number(api_json_placeholder):
    pr = post_requests()
    response = pr.delete_post(api_json_placeholder, "1")
    assert response.status_code == ApiHttpConstants.OK
