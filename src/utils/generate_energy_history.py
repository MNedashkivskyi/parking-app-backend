from datetime import datetime, timedelta
from random import random
from math import sin, pi

def energy_demand_function(x: float):
    return -sin((0.00225 * x + 0.5) ** 2 + pi / 4) + 3 * sin(((0.00229 * x + 0.3) / 3.6) ** 3 * pi) + 16

now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=11)

# Creating 10 similar functions to energy_demand_function
for day in range(10):
    sin_rand = random() * 2 - 1
    rand = random() * 2 - 1
    for i in range(1440):
        value = energy_demand_function(i) + sin_rand * sin(pi * i / 720) - rand
        print(f"INSERT INTO energy_history (post_date, value) VALUES('{now}.000000', {value});")
        if i % 60 == 0:
            print("commit;")
        now += timedelta(minutes=1)
