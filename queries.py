from datetime import timedelta

import graphene
import bcrypt
from graphql import GraphQLError
from jwt import PyJWTError
from utils import create_access_token, decode_access_token
from pydantic import ValidationError

import models
from schemas import PostModel, PostSchema, UserSchema
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

class AuthenticateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    token = graphene.String()

    @staticmethod
    def mutate(root, info, username, password):

        user = UserSchema(username=username, password=password)

        db_user_info = db.query(models.User).filter(models.User.username == username).first()

        if bcrypt.checkpw(user.password.encode("utf-8"), db_user_info.password.encode("utf-8")):
          access_token_expires = timedelta(minutes=60)
          access_token = create_access_token(data={"user": username}, expires_delta=access_token_expires)
          return AuthenticateUser(ok=True, token=access_token)
        return AuthenticateUser(ok=False)


class CreateNewUser(graphene.Mutation):
  class Arguments:
    username = graphene.String(required=True)
    password = graphene.String(required=True)

  ok = graphene.Boolean()
  msg = graphene.String()

  @staticmethod
  def mutate(root, info, username, password):

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    password_hash = hashed_password.decode("utf8")
    
    try:
      user = UserSchema(username=username, password=password_hash)
      db_user = models.User(username=user.username, password=password_hash)
    except  ValidationError as e:
      return CreateNewUser(ok=False, msg=e)

    try:
      db.add(db_user)
      db.commit()
      db.refresh(db_user)
      return CreateNewUser(ok=True, msg=user.username)
    except:
      db.rollback()
      db.close()
      return CreateNewUser(ok=False)


class CreateNewPost(graphene.Mutation):
  class Arguments:
      title = graphene.String(required=True)
      content = graphene.String(required=True)
      token = graphene.String(required=True)
      author = graphene.String()

  ok = graphene.Boolean()
  msg = graphene.String()

  @staticmethod
  def mutate(root, info, title, content, token, author=""):
    try:
      payload = decode_access_token(data=token)
      username = payload.get("user")
      if username is None:
        raise GraphQLError("Invalid credentials")
    except PyJWTError:
      raise GraphQLError("Invalid token provided")

    user = db.query(models.User).filter(models.User.username == username).first()

    if user is None:
      raise GraphQLError("Invalid user credentials")
    
    try:
      post = PostSchema(title=title, content=content, author=author, user_id=user.id)
      db_post = models.Post(title=post.title, content=post.content, author=post.author, user_id=post.user_id)
    except  ValidationError as e:
      return CreateNewPost(ok=False, msg=e)

    try:
      db.add(db_post)
      db.commit()
      db.refresh(db_post)
      return CreateNewPost(ok=True)
    except:
      db.rollback()
      return CreateNewPost(ok=False, msg=post.content)


class PostMutations(graphene.ObjectType):
  authenticate_user = AuthenticateUser.Field()
  create_new_user = CreateNewUser.Field()
  create_new_post = CreateNewPost.Field()
  

schema = graphene.Schema(query=Query, mutation=PostMutations)