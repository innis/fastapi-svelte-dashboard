import random
import uuid

def code_generator(size=12):
    n = 4
    x = str(uuid.uuid4()).replace("-","") # 36 length uuid string
    start = random.randrange(len(x)-size)
    code = (x[start:start+size]).upper()
    return '-'.join([code[i:i+n] for i in range(0, len(code), n)])
