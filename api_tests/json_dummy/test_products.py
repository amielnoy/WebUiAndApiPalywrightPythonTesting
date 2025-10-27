from api_tests.globals import ApiHttpConstants
from api_tests.json_dummy.products_service import products_requests


def test_get_products_count(api_json_dummy):
    pr=products_requests()
    response = pr.get_all_products(api_json_dummy)
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    assert data['total'] == 194

def test_get_post_number(api_json_dummy):
    pr = products_requests()
    response = pr.get_product_by_number(api_json_dummy, "1")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    assert data['id'] == 1,"error is user id,expected 1"
    assert data['title'] == 'His mother had always taught him'
    assert data['body'] == 'His mother had always taught him not to ever think of himself as better than others. He\'d tried to live by this motto. He never looked down on those who were less fortunate or who had less money than him. But the stupidity of the group of people he was talking to made him change his mind.'
    assert data['tags'] == ['history', 'american', 'crime']
    assert data['reactions'] == {'dislikes': 25, 'likes': 192}
def test_add_product(api_json_dummy):
    payload = {
        "id": 195,
        "title": "iPhone 17 Pro",
        "description": "iPhone 17 Pro 2025 model",
        "price": 1499,
        "category": "smartphones",
        "brand": "Apple",
        "tags": ["Apple", "smartphone", "usa-model"],
    }
    product_requests = products_requests()
    response = product_requests.create_product(api_json_dummy, payload)
    assert response.status_code == ApiHttpConstants.CREATED
    data = response.json()
    assert data['id'] == payload['id'], "error is user id,expected 1"
    assert data['title'] == payload['title'],'error in title'
    assert data['description'] == payload['description'],'error in description'
    assert data['price'] == payload['price'],'error in price'
    assert data['category'] == payload['category'],'error in category'
    assert data['brand'] == payload['brand'],'error in brand'

def test_update_product(api_json_placeholder):
    updated_payload = {
        "id": 1,
        "title": "Updated title",
        "body": "Updated body"
    }
    pr = products_requests()
    response = pr.update_product(api_json_placeholder, updated_payload,1)
    assert response.status_code == ApiHttpConstants.OK
    assert response.json()["title"] == updated_payload['title']
    assert response.json()["body"] == updated_payload['body']

def test_delete_product_by_id(api_json_placeholder):
    pr = products_requests()
    response = pr.delete_product(api_json_placeholder, "1")
    assert response.status_code == ApiHttpConstants.OK


