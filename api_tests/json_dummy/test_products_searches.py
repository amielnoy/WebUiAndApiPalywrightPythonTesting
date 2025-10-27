from api_tests.globals import ApiHttpConstants
from api_tests.json_dummy.products_service import products_requests

def test_get_products_by_query(api_json_dummy):
    pr=products_requests()
    response = pr.get_products_by_query(api_json_dummy,"phones")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    # Top-level structure assertions
    assert isinstance(data, dict)
    assert data["total"] == 4
    assert data["limit"] == 4
    assert data["skip"] == 0
    assert "products" in data and isinstance(data["products"], list)
    assert len(data["products"]) == 4

    first = data["products"][0]

    expected_first = {
        "availabilityStatus": "In Stock",
        "brand": "Apple",
        "category": "mobile-accessories",
        "description": "The Apple AirPods Max in Silver are premium over-ear headphones with high-fidelity audio, adaptive EQ, and active noise cancellation. Experience immersive sound in style.",
        "dimensions": {"depth": 27.54, "height": 14.9, "width": 24.88},
        "discountPercentage": 13.67,
        "id": 101,
        "images": ["https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpods-max-silver/1.webp"],
        "meta": {
            "barcode": "4062176053732",
            "createdAt": "2025-04-30T09:41:02.053Z",
            "qrCode": "https://cdn.dummyjson.com/public/qr-code.png",
            "updatedAt": "2025-04-30T09:41:02.053Z",
        },
        "minimumOrderQuantity": 1,
        "price": 549.99,
        "rating": 3.47,
        "returnPolicy": "No return policy",
        "reviews": [
            {
                "comment": "Excellent quality!",
                "date": "2025-04-30T09:41:02.053Z",
                "rating": 5,
                "reviewerEmail": "henry.adams@x.dummyjson.com",
                "reviewerName": "Henry Adams",
            },
            {
                "comment": "Very happy with my purchase!",
                "date": "2025-04-30T09:41:02.053Z",
                "rating": 4,
                "reviewerEmail": "elijah.cruz@x.dummyjson.com",
                "reviewerName": "Elijah Cruz",
            },
            {
                "comment": "Would buy again!",
                "date": "2025-04-30T09:41:02.053Z",
                "rating": 4,
                "reviewerEmail": "william.lopez@x.dummyjson.com",
                "reviewerName": "William Lopez",
            },
        ],
        "shippingInformation": "Ships in 2 weeks",
        "sku": "MOB-APP-APP-101",
        "stock": 59,
        "tags": ["electronics", "over-ear headphones"],
        "thumbnail": "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpods-max-silver/thumbnail.webp",
        "title": "Apple AirPods Max Silver",
        "warrantyInformation": "No warranty",
        "weight": 2,
    }

    assert first == expected_first, f"First product mismatch.\nGot: {first}\nExpected: {expected_first}"

def test_get_post_number1(api_json_dummy):
    pr = products_requests()
    response = pr.get_product_by_number(api_json_dummy, "1")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    assert data['id'] == 1,"error is user id,expected 1"
    assert data['title'] == 'His mother had always taught him'
    assert data['body'] == 'His mother had always taught him not to ever think of himself as better than others. He\'d tried to live by this motto. He never looked down on those who were less fortunate or who had less money than him. But the stupidity of the group of people he was talking to made him change his mind.'
    assert data['tags'] == ['history', 'american', 'crime']
    assert data['reactions'] == {'dislikes': 25, 'likes': 192}


def test_search_products_by_query(api_json_dummy):
    min_price = 50
    max_price = 100
    pr=products_requests()
    response = pr.filter_products_by_price(api_json_dummy,min_price,max_price,"title,price")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    # Top-level structure assertions
    assert isinstance(data, dict)
    assert data["total"] == 194
    assert data["limit"] == 50
    assert data["skip"] == 100
    assert "products" in data and isinstance(data["products"], list)
    assert len(data["products"]) == 50

def test_products_sorted_by_title_asc(api_json_dummy):
    pr = products_requests()
    resp = pr.filter_sort_products(api_json_dummy, sort_by="title", order="asc", limit=3, skip=0)
    assert resp.status_code == ApiHttpConstants.OK

    data = resp.json()
    assert "products" in data and isinstance(data["products"], list)
    assert len(data["products"]) == 3
    for product in data["products"]:
        print(product['title'])

    titles = [p["title"] for p in data["products"]]
    assert titles == sorted(titles, key=str.lower)
    for title in titles:
        print(title)


def test_get_products_by_category_smartphones(api_json_dummy):
    pr = products_requests() # Use API client directly for the category path, or add a service method if you prefer
    response = pr.get_products_by_category(api_json_dummy,"smartphones",3,0,sort_by='title',order="asc")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    # Top-level structure assertions
    assert isinstance(data, dict)
    assert "products" in data and isinstance(data["products"], list)
    assert "total" in data and isinstance(data["total"], int)
    assert "skip" in data and isinstance(data["skip"], int)
    assert "limit" in data and isinstance(data["limit"], int)

    products = data["products"]
    assert len(products) > 0, "Expected at least one smartphone product"

    # Validate each product belongs to the requested category and has basic fields
    for p in products:
        assert p.get("category") == "smartphones"
        assert isinstance(p.get("id"), int)
        assert isinstance(p.get("title"), str)
        assert isinstance(p.get("price"), float)
        # Optional: tags is a list when present
        if "tags" in p:
            assert isinstance(p["tags"], list)

    # Optional: verify sorting by title asc on this slice
    titles = [p["title"] for p in products]
    assert titles == sorted(titles, key=str.lower), "Expected smartphones page to be sorted by title asc when requested"

