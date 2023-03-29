from datetime import datetime

start_time = datetime.now()

def log(*msg):
    global start_time

    current_time = datetime.now()
    s = ''
    for _ in msg:
        s += f'{_}  '
    ts = '%s' % str(current_time - start_time).split('.')[0]
    print(f"{ts} - {s}")
    last_time = current_time


def format_time(t:datetime):
    return t.strftime("%H:%M:%S")
