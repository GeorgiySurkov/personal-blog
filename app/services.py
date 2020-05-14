from typing import List


def parse_tags(tags: str) -> List[str]:
    tags = tags.split(',')
    parsed_tags = []
    for tag in tags:
        if len(tag) > 0:
            parsed_tags.append(' '.join(tag.strip().split()).capitalize())
    return parsed_tags
