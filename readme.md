# FastAPI REST and GraphQL CRUD SERVER 

> Simple containerized fastapi server with a postgres database consisting of both REST and GraphQL endpoints.

## Technologies

### Stack
Project is created with: 
* Docker
* Python
* FastAPI
* Postgres
* Redis
* Celery
* Flower

### Packages
Project uses the following packages: 
* bcrypt
* SQLAlchemy
* graphene
* alembic
* pydantic

## Setup
Run `docker compose up` in project root directory

- **visit localhost:8080/ for the server**
- **visit localhost:5050/ for pg admin**
- **visit localhost:5555/ for flower**

### API doc 

#### Rest
Visit the documentation endpoint to see the swagger docs.
Available at [/docs]((http://localhost:8080/docs) running project locally

The task queue can be interacted with by making a post request to /reverse and providing a body consisting of:
- delay(int) -> time in seconds to delay the task by
- text(string) -> any text to be reversed

**NB** The task queue runs synchronously as it blocks for the number of seconds specified. It is just a proof of concept; can't think of any basic use for it in this project.

#### graphql commands
The graphql endpoint is available at [/graphql](http://localhost:8080/graphql)

##### Queries
query{
  allPosts{
    title
    author
    content
    userId
  }
}

query{
  postById(postId:9){
    title
    author
    content
    userId
  }
}

##### Mutations
mutation CreateNewUser{
  createNewUser(username:"", password:"") {
    ok
	msg
  }
}

mutation AuthenticateUser{
  authenticateUser(username:"", password:"") {
    ok
	token
  }
}

mutation CreateNewPost{
  createNewPost(title:"", content:"", token: "") {
    ok
	msg
  }
}