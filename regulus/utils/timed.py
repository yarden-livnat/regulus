from time import process_time

def timed(method):
    def _timed(*args, **kwargs):
        start = process_time()
        value = method(*args, **kwargs)
        end = process_time()

        print(f'{end-start:.2f}ms')
        return value
    return _timed
