# --- Open cmt line bellow if run by cmd: python *.py
# import sys  # nopep8
# sys.path.append(".")  # nopep8
# ----
print("ok1")
import json
import random
import time
from datetime import datetime

import numpy as np
print("ok2")
from settings import TRANSACTIONS_TOPIC, DELAY, OUTLIERS_GENERATION_PROBABILITY
print("ok3")
from utils import create_producer
print("ok4")
_id = 0
producer = create_producer()

if producer is not None:
    while True:
        print(_id)
        # Generate some abnormal observations
        if random.random() <= OUTLIERS_GENERATION_PROBABILITY:
            X_test = np.random.uniform(low=-4, high=4, size=(1, 2))
        else:
            X = 0.3 * np.random.randn(1, 2)
            X_test = (X + np.random.choice(a=[2, -2], size=1, p=[0.5, 0.5]))

        X_test = np.round(X_test, 3).tolist()

        current_time = datetime.utcnow().isoformat()

        record = {"id": _id, "data": X_test, "current_time": current_time}
        record = json.dumps(record).encode("utf-8")

        producer.produce(topic=TRANSACTIONS_TOPIC,
                         value=record)
        producer.flush()
        _id += 1
        # time.sleep(DELAY)
        time.sleep(1)
