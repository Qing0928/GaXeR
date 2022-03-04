import time
from datetime import datetime

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
now_stamp = int(time.mktime(struct_time))
print(now)
print(now_stamp)