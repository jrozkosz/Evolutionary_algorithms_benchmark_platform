from locust import HttpUser, TaskSet, task, between
from time import sleep

class UserBehavior(TaskSet):
    @task
    def upload_file(self):
        self.client.post('/login', json={
            "email": "admin",
            "password": "admin"
        })
        with open('algorithm.py', 'rb') as f:
            self.client.post('/upload', files={'file': f})

        self.client.get("/upload/progress")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(9, 10)