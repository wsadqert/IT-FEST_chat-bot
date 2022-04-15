import vk
from tokens import ACCESS_TOKEN


def get_posts(owner_id: int, count: int, offset: int) -> dict:
	posts: dict = vk_api.wall.get(owner_id=owner_id, v=5.131, count=count, offset=offset)
	print(posts)
	return posts


def post_text(post: dict) -> str:
	return post['items'][0]['text']


session = vk.Session(ACCESS_TOKEN)
vk_api = vk.API(session)
