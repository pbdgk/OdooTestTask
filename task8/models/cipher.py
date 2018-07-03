import threading
import queue
import random


class Cipher:

    extension = '.enc'

    def __init__(self, chunk_size=1024*64, threads=4):
        self.chunk_size = chunk_size
        self.threads = threads
        self.lock = threading.Lock()
        self.queue = queue.Queue()

    def cipher(self, in_file, out_file, encoder):
        self._spawn_threads(in_file, out_file, encoder)

    def decipher(self, in_file, out_file, decoder):
        self._spawn_threads(in_file, out_file, decoder)

    def _spawn_threads(self, in_file_, out_file_, action):
        with open(in_file_, 'rb') as in_file, open(out_file_, 'wb') as out_file:
            threads = []
            for i in range(self.threads):
                t = threading.Thread(target=self._run,
                                     args=(in_file, out_file, action)
                                     )
                threads.append(t)
                t.start()
            for thread in threads:
                thread.join()

    def _run(self, in_file, out_file, action):
        while True:
            with self.lock:
                chunk = self._read_chunk(in_file)
                if not chunk:
                    break
                self.queue.put(chunk)
            with self.lock:
                chunk = self.queue.get()
                processed_chunk = action(chunk)
                out_file.write(processed_chunk)

    def _read_chunk(self, file):
        data = file.read(self.chunk_size)
        return data
