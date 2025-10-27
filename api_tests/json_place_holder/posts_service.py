from api_tests.globals import ApiHttpConstants

class post_requests():
    def get_all_posts(self,api):
        response = api.get("posts")
        return response

    def get_post_by_number(self,api,post_number):
        response = api.get("posts/"+post_number)
        return response
    def create_post(self,api,payload):
        response = api.post("posts", data=payload)
        return response

    def update_post(self,api,payload):
        response = api.put("posts/1", data=payload)
        return response

    def delete_post(self,api,post_number):
        response = api.delete("posts/"+post_number)
        return response
