# author: Jakub Rozkosz

from locust import HttpUser, TaskSet, task, between
from time import sleep

class UserBehavior(TaskSet):
    @task
    def login_logout(self):
        self.client.post('/login', json={
            "email": "admin",
            "password": "admin"
        })
    
    @task
    def display_information(self):
        self.client.get("/information")
    
    @task
    def display_rankings(self):
        self.client.get("/algorithms_rankings")
        
    # @task
    # def display_rankings(self):
    #     self.client.post("/logout")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
