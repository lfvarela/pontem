import threading

def process_threaded(call, args_list, num_workers=8):

    def thread_target():
        global c
        global num_done
        while True:
            c.acquire()
            remaining = len(args_list)
            if remaining == 0:
                num_done += 1
                if num_done == num_workers:
                    c.notify_all()
                c.release()
                return

            args = args_list.pop()
            c.release()
            idx, result = call(*args)
            if result:
                results[idx] = result

    global c
    c = threading.Condition()
    c.acquire()

    # Start and join threads
    threads = [threading.Thread(target=thread_target) for _ in range(num_workers)]

    global num_done
    num_done = 0

    global results
    results = {}

    for t_id, t in enumerate(threads):
        t.start()
    c.wait()
    c.release()
    for t_id, t in enumerate(threads):
        threads[t_id].join()

    return results