from globals import ApiHttpConstants
from json_place_holder.todos_service import todos_requests


def test_get_todo_by_number(api_json_placeholder):
    to_dos_service=todos_requests()
    response = to_dos_service.get_post_by_number(api_json_placeholder,"1")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    assert data["userId"] == 1
    assert data["title"] == "delectus aut autem"
    assert isinstance(data["completed"],bool)

def test_create_new_todo(api_json_placeholder):
    payload = {
        "userId": 1,
        "title": "New xyte post",
        "body": "This is a body of the xyte post"
    }
    to_dos_service=todos_requests()
    response = to_dos_service.create_todo(api_json_placeholder, payload)
    assert response.status_code == ApiHttpConstants.CREATED
    data = response.json()
    assert data["title"] == payload["title"], "data <> payload!"
#should fail json place holder doesn't persist the delete!!
def test_delete_todo(api_json_placeholder):
    to_dos_service = todos_requests()
    response = to_dos_service.delete_todo(api_json_placeholder,"1")
    response.status_code=ApiHttpConstants.DELETED
    response = to_dos_service.get_post_by_number(api_json_placeholder,"1")
    assert response.status_code == ApiHttpConstants.NOT_FOUND