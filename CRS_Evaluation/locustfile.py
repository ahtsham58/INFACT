import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    def on_start(self):
        self.client.post("/", {"readit":"1"})

    @task
    def rate_items(self):
            with self.client.get("/ratings.html") as response:
                if response-status_code == 404:
                    response.success()
                    for i in range(10):
                        self.client.post("/ratings.html", {"rating1":"1","response1":"abc","rating2":"5","response2":"abc","rating3":"3","response3":"abc"})
                        print("executing my_task")


