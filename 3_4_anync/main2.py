import multiprocessing, time, random


def hello(delay: int, msg: str, child_node: multiprocessing.Pipe):
    time.sleep(delay)
    child_node.send(1)
    child_node.close()
    print(f"{delay} Hello. {msg}")


count = 0


def main():
    proc = []
    # multiprocessing.Queue()
    for _ in range(5):
        par_node, child_node = multiprocessing.Pipe()
        # proc.append(multiprocessing.Process(target=hello, args=(random.randint(1, 5), "H")))
        proc.append(multiprocessing.Process(target=hello, args=(random.randint(1, 5), "H", child_node)))
        proc.append(
            {
                "proc": multiprocessing.Process(target=hello, args=(random.randint(1, 5), "H", child_node)),
                "pipe": par_node
            }
        )
        # proc.append(multiprocessing.Process(target=hello, args=(random.randint(1, 5), "H", child_node)))
        proc[-1]["proc"].start()
    for p in proc:
        p.join()
    global count
    print(count)
    

if __name__ == "__main__":
    main()