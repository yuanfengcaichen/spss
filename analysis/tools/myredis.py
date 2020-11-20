from django_redis import get_redis_connection

def getconn():
    conn = get_redis_connection("default")
    return conn
