
from fields.extras import ValidationError
from schema import Schema
from marshmallow import Schema, fields, ValidationError

from api_tests.globals import ApiHttpConstants


def test_get_posts_count(api_json_placeholder):
    response = api_json_placeholder.get("users/1/albums")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    assert len(data) == 10

def test_get_user_albom_number_2(api_json_placeholder):
    response = api_json_placeholder.get("users/1/albums")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    assert data[2]['userId'] == 1,"error in user id,expected 3"
    assert data[2]['id'] == 3,"error is user id,expected 3"
    assert data[2]['title'] == "omnis laborum odio"

def test_user_albums_schema(api_json_placeholder):
    """
    Validates that each album in the response has the correct schema:
    - id: int
    - title: str
    - userId: int
    """
    response = api_json_placeholder.get("users/1/albums")
    assert response.status_code == ApiHttpConstants.OK
    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    for album in data:
        assert isinstance(album, dict), f"Album is not a dict: {album}"
        assert set(album.keys()) == {"id", "title", "userId"}, f"Unexpected keys: {album.keys()}"
        assert isinstance(album["id"], int), f"id is not int: {album['id']}"
        assert isinstance(album["title"], str), f"title is not str: {album['title']}"
        assert isinstance(album["userId"], int), f"userId is not int: {album['userId']}"

class AlbumSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    userId = fields.Int(required=True)

def test_user_albums_schema_with_marshmellow(api_json_placeholder):
    """
    Test that the user albums API returns data matching the expected schema.
    """
    response = api_json_placeholder.get("/albums")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "Response should be a list of albums"

    schema = AlbumSchema()
    for album in data:
        try:
            schema.load(album)
        except ValidationError as err:
            assert False, f"Schema validation failed for album: {album}\nErrors: {err.messages}"
