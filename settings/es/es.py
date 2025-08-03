from elasticsearch import Elasticsearch




class Article_es:

    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    async def article(self, post):
        doc = {
            "article_uuid": post.uuid,
            "title": post.title,
            "username": post.username,
            "category_name": post.category_name,
            "tag_names": post.tag_names,
            "is_published": post.is_published,
            "created_at": post.created_at.isoformat(),
        }
        self.es.index(index="blog_post", id=post.id, document=doc)