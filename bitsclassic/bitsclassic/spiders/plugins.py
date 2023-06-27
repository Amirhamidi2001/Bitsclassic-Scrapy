import uuid

def gen_random_id():
    return str(uuid.uuid4()).split("-")[0]
