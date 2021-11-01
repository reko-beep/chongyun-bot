from datetime import datetime
import inspect



def log(*msg):
    current_time = datetime.now().strftime("%m %b %H:%M:%S")
    print(f'[{current_time}]', *msg)


def logc(*msg):
    stack = inspect.stack()
    class_name = stack[1][0].f_locals["self"].__class__.__name__
    log(f'[{class_name}]', *msg)