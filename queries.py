import graphene

import models
from schemas import PostModel, PostSchema
from db_conf import db_session

db = db_session.session_factory()

class Query(graphene.ObjectType):

  all_posts = graphene.List(PostModel)
  post_by_id = graphene.Field(PostModel, post_id=graphene.Int(required=True))

  def resolve_all_posts(self, info):
      query = PostModel.get_query(info)
      return query.all()

  def resolve_post_by_id(self, info, post_id):
      return db.query(models.Post).filter(models.Post.id == post_id).first()


class CreateNewPost(graphene.Mutation):
  class Arguments:
      title = graphene.String(required=True)
      content = graphene.String(required=True)
      author = graphene.String()
      userId = graphene.Int(required=True)

  ok = graphene.Boolean()

  @staticmethod
  def mutate(root, info, title, content, author, userId):
      post = PostSchema(title=title, content=content, author=author, user_id=userId)
      db_post = models.Post(title=post.title, content=post.content, author=post.author, user_id=post.user_id)
      try:
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return CreateNewPost(ok=True)
      except:
        db.rollback()
        return CreateNewPost(ok=False)


class PostMutations(graphene.ObjectType):
  create_new_post = CreateNewPost.Field()
  

schema = graphene.Schema(query=Query, mutation=PostMutations)