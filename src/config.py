import os

class Env:
    url = os.getenv("DATABASE_URL")
    key = os.getenv("key")
    

