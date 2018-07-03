import threading
import queue
import operator

import time
import random

FILE_NAME = '1.png'
SECRET_KEY = 'asdfasdfzxcv2)()@*$__FSAdfcv'


class Cipher:

    extension = '.enc'

    def __init__(self, secret, chunk_size=1024*64, threads=4):
        self.secret = secret
        self.chunk_size = chunk_size
        self.threads = threads
        self.lock = threading.Lock()
        self.queue = queue.Queue()

    def cipher(self, in_file, out_file):
        self._spawn_threads(in_file, out_file, operator.add)

    def decipher(self, in_file, out_file):
        self._spawn_threads(in_file, out_file, operator.sub)

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

    def _run(self, in_file, out_file, operator):
        while True:
            with self.lock:
                chunk = self._read_chunk(in_file)
                if not chunk:
                    break
                self.queue.put(chunk)
            with self.lock:
                chunk = self.queue.get()
                processed_chunk = self._process_chunk(chunk, operator)
                out_file.write(processed_chunk)

    def _read_chunk(self, file):
        data = file.read(self.chunk_size)
        return data

    def _process_chunk(self, chunk, operator_):
        """
        operator must be operator.add | operator.sub
        add consider for cypher chunk
        sub consider for decypher chunk
        """
        byte_array_chunk = bytearray(chunk)
        for index, byte in enumerate(byte_array_chunk):
            salt = ord(self.secret[index % len(self.secret)])
            processed_byte = operator_(byte, salt) % 256
            byte_array_chunk[index] = processed_byte
        return byte_array_chunk


if __name__ == '__main__':
    cipher = Cipher(SECRET_KEY)
    out_file = FILE_NAME + cipher.extension
    cipher.cipher(FILE_NAME, out_file)
    cipher.decipher(FILE_NAME + cipher.extension, 'decoded-' + FILE_NAME)
