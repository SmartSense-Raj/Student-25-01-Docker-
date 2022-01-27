# Student-25-01-Docker-

Here, I have created FastAPI for student management to perform CRUD operation.
I have used mysql-server, which is running on the localhost.
To containerise FastAPI, I've used dokcer.

The task was to access mysql-server(located inside localhost) from container and perform CRUD operations.

USED Docker command:
 - docker build --tag token .
 - docker run --name raj --network=host token
