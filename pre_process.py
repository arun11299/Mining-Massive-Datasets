import sys
import time
import hashlib
from memory_profiler import profile

store = dict()

@profile
def read_file():
    global store
    start_time = time.time()
    fd = open('processed_file.txt', 'wb')
    with open("sentences.txt", 'r') as f:
        for line in f:
            line = line.rstrip()
            ## Remove the numeric identifier from the line
            parsed = line.split(' ', 1)[1]
            if not store.has_key(hashlib.sha256(parsed).hexdigest()):
                fd.write(parsed + '\n')
                store[hashlib.sha256(parsed).hexdigest()] = True
            else:
                pass
    fd.close()
    elapsed_time = time.time() - start_time
    print "Elapsed time is: %s" % str(elapsed_time)

if __name__ == "__main__":
    read_file()

