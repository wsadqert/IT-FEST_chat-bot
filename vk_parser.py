import vk
from src.tokens import ACCESS_TOKEN


def get_posts(owner_id: int, count: int, offset: int) -> dict:
	posts: dict = vk_api.wall.get(owner_id=owner_id, v=5.131, count=count, offset=offset)
	return posts


def post_text(post: dict) -> str:
	return post['items'][0]['text']


def last_post_id(owner_id: int) -> int:
	return get_posts(owner_id, 1, 0)['items'][0]['id']


session = vk.Session(ACCESS_TOKEN)
vk_api = vk.API(session)
