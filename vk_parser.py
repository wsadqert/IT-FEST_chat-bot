import vk
from database import *
from constants import *
from rich.traceback import install
install(show_locals=True, width=300)


def get_posts(owner_id: str, count: int, offset: int):
	posts = vk_api.wall.get(owner_id=owner_id, v=5.92, count=count, offset=offset)
	print(posts)
	return posts


session = vk.Session(access_token)
vk_api = vk.API(session)
group_id: str = ...
owner_id: str = ...

get_posts(owner_id, 10, 0)

