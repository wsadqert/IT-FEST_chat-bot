import vk
from constants import owner_ids
from tokens import ACCESS_TOKEN


def get_posts(owner_id: int, count: int, offset: int):
    posts = vk_api.wall.get(owner_id=owner_id, v=5.131, count=count, offset=offset)
    print(posts)
    return posts


session = vk.Session(ACCESS_TOKEN)
vk_api = vk.API(session)

for owner_id in owner_ids:
    get_posts(owner_id, 10, 0)
