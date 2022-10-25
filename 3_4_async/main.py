import threading, time, random


def hello(delay: int, msg: str, lock: threading.Lock):
    with lock:
    # lock.acquire()
        global count
        old_count = count
        time.sleep(delay)
        count = old_count + 1
    # lock.release()
    time.sleep(delay)
    print(f"{delay} Hello. {msg}")


count = 0


def main():
    threads = []
    lock = threading.Lock()
    for _ in range(5):
        threads.append(threading.Thread(target=hello, args=(random.randint(1, 5), "H", lock)))
        threads[-1].start()
    
    for t in threads:
        t.join()
    global count
    print(count)
    

if __name__ == "__main__":
    main()