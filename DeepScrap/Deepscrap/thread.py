from queue import Queue

from threading import Thread


class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()


class ThreadPool:
    # queue안에 있는 thread에 작업할당
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        # 
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        self.tasks.join()


if __name__ == "__main__":
    from random import randrange
    from time import sleep
    import subprocess

    def username(d):
        subprocess.call(['scrapy', 'crawl_many', '-a', 'd', '-o', 'output.json', '-t','json'])
        sleep(1) 
    # Generate random delays
    with open('search_list.txt','r') as f:
        l = f.read().split(',')
        
        user_list = [user for user in l if user is not '']

        pool = ThreadPool(5)

        pool.map(username, user_list)
        pool.wait_completion()
