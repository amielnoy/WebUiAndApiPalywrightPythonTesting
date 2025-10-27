from api_tests.globals import ApiHttpConstants
from api_tests.json_dummy.products_service import products_requests

def test_get_product_by_invalid_id_returns_404(api_json_dummy):
    pr = products_requests()
    resp = api_json_dummy.get("products/999999")
    assert resp.status_code == ApiHttpConstants.NOT_FOUND
    data = resp.json()
    assert "message" in data or "error" in data

#negative test fails
def test_create_product_missing_required_fields_returns_400(api_json_dummy):
    pr = products_requests()
    # Missing title and price
    payload = { "category": "smartphones", "brand": "Apple", }
    resp = pr.create_product(api_json_dummy, payload)
    assert resp.status_code == ApiHttpConstants.BAD_REQUEST
    data = resp.json()
    assert "message" in data or "errors" in data

#negtive test should fail
def test_create_product_with_wrong_types_returns_400(api_json_dummy):
    pr = products_requests()
    # price must be number, tags must be list
    payload = { "title": "Bad Product",
                "description": "Wrong types",
                "price": "one hundred",
                # wrong type
                "category": "smartphones",
                "brand": "Apple",
                "tags": "not-a-list",
               }
    resp = pr.create_product(api_json_dummy, payload)
    assert resp.status_code == ApiHttpConstants.BAD_REQUEST
    data = resp.json()
    assert "message" in data or "errors" in data

def test_update_non_existing_product_returns_404(api_json_dummy):
    pr = products_requests()
    payload = {"title": "Will not update"}
    resp = pr.update_product("products/999999", data=payload)
    assert resp.status_code == ApiHttpConstants.NOT_FOUND

def test_delete_non_existing_product_returns_404(api_json_dummy):
    pr = products_requests()
    resp = api_json_dummy.delete("products/999999")
    assert resp.status_code == ApiHttpConstants.NOT_FOUND

def test_search_products_no_match_returns_empty_list(api_json_dummy):
    pr = products_requests()
    q = "this-query-should-not-match-anything-xyz"
    resp = pr.get_products_by_query(api_json_dummy, q)
    assert resp.status_code == ApiHttpConstants.OK
    data = resp.json()
    assert "products" in data and isinstance(data["products"], list)
    assert data["total"] == 0
    assert data["products"] == []

def test_filter_products_invalid_price_range(api_json_dummy):
    pr = products_requests()
    # If API returns 400 for invalid ranges, assert BAD_REQUEST; otherwise allow empty result with 200
    resp = api_json_dummy.get("products/filter?priceMin=500&priceMax=100")
    if resp.status_code == ApiHttpConstants.BAD_REQUEST:
        assert True
    else:
        assert resp.status_code == ApiHttpConstants.OK
    data = resp.json()
    assert "products" in data and isinstance(data["products"], list)
    for p in data["products"]: assert float(p["price"]) >= 100 # basic sanity if server normalized inputs

def test_get_products_unknown_category_returns_404(api_json_dummy):
    pr = products_requests()
    resp = api_json_dummy.get("products/category/not-a-real-category")
    assert resp.status_code == ApiHttpConstants.NOT_FOUND

