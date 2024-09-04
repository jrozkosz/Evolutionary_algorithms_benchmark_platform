# author: Jakub Rozkosz

from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        self.login_and_upload()

    def login_and_upload(self):
        self.client.post('/login', json={
            "email": "admin",
            "password": "admin"
        })
        
        with open('algorithm.py', 'rb') as f:
            self.client.post('/upload', files={'file': f})

    @task
    def check_progress(self):
        self.client.get("/upload/progress")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 6)
