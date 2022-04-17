import vk
from src.tokens import ACCESS_TOKEN

POST = dict


def get_posts(owner_id: int, count: int, offset: int) -> dict:
	return vk_api.wall.get(owner_id=owner_id, v=5.131, count=count, offset=offset)


def post_text(post: POST) -> str:
	return post['text']


def last_post(owner_id: int) -> POST:
	return get_posts(owner_id, 1, 0)['items'][0]


session = vk.Session(ACCESS_TOKEN)
vk_api = vk.API(session)
