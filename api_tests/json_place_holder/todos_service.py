from api_tests.globals import ApiHttpConstants

class todos_requests():
    def get_all_posts(self,api):
        response = api.get("todos")
        return response

    def get_post_by_number(self,api,post_number):
        response = api.get("todos/"+post_number)
        return response
    def create_todo(self,api,payload):
        response = api.post("todos", data=payload)
        return response

    def update_todo(self,api,payload):
        response = api.put("todos/1", data=payload)
        return response

    def delete_todo(self,api,post_number):
        response = api.delete("todos/"+post_number)
        return response
