import multiprocessing

bind = "0.0.0.0:3000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2