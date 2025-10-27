from typing import Any, Dict, Optional, Tuple

class products_requests():
    def get_all_products(self,api):
        response = api.get("products")
        return response

    def get_product_by_number(self,api,product_number):
        response = api.get("posts/"+product_number)
        return response
    def create_product(self, api, payload):
        response = api.post("products/add", data=payload)
        return response

    def update_product(self, api, payload,product_number):
        response = api.put(f"posts/{product_number}", data=payload)
        return response

    def delete_product(self, api, post_number):
        response = api.delete("posts/"+post_number)
        return response

    def get_products_by_query(self,api,query):
        response = api.get("products/search?q="+query)
        return response

    def filter_products_by_price(self, api, limit: str, skip: str, query: str = None):
            """
            Filter products by price range using DummyJSON's /products/filter endpoint.
            Optionally include a search query 'q' to combine title/description search with price range.

            Args:
                api: APIClient instance (from your fixtures) exposing .get(path: str)
                min_price: minimum price (inclusive)
                max_price: maximum price (inclusive)
                query: optional free-text search term

            Returns:
                API response object
            """
            path = f"products?limit={limit}&skip={skip}"
            if query:
                path += f"&select={query}"
            return api.get(path)

    def filter_sort_products(self, api, sort_by: str, order: str = "asc", limit: int = 30,
                             skip: int = 0):
        path = f"products?sortBy={sort_by}&order={order}&limit={limit}&skip={skip}"
        return api.get(path)

    def get_products_by_category(self, api, category: str, limit: int = 30, skip: int = 0,
                                 sort_by: Optional[str] = None, order: str = "asc"):
        """
        Fetch products by category using DummyJSON's /products/category/{category} endpoint,
        with optional pagination and sorting.

        Args:
            api: APIClient instance exposing .get(path: str)
            category: category slug (e.g., "smartphones")
            limit: page size (default 30)
            skip: offset for pagination (default 0)
            sort_by: optional field to sort by (e.g., "title", "price", "rating")
            order: "asc" or "desc" when sort_by is provided

        Returns:
            API response object from the GET request.
        """
        path = f"products/category/{category}?limit={limit}&skip={skip}"
        if sort_by:
            path += f"&sortBy={sort_by}&order={order}"
        return api.get(path)
