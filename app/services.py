from typing import List
from itertools import islice


def parse_tags(tags: str) -> List[str]:
    tags = tags.split(',')
    parsed_tags = []
    for tag in tags:
        if len(tag) > 0:
            parsed_tags.append(' '.join(tag.strip().split()).capitalize())
    return parsed_tags


def list_most_frequent_tags(posts, limit=5):
    tag_amount = {}
    for post in posts:
        for tag in post.tags:
            if tag in tag_amount:
                tag_amount[tag] += 1
            else:
                tag_amount[tag] = 1
    return map(
        lambda item: item[0],
        islice(
            sorted(tag_amount.items(), key=lambda x: x[1], reverse=True),
            0,
            limit
        )
    )
