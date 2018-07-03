import operator


class Private:
    def __init__(self, secret):
        self.secret = secret

    def encoder(self, chunk):
        return self._process_chunk(chunk, operator.add)

    def decoder(self, chunk):
        return self._process_chunk(chunk, operator.sub)

    def _process_chunk(self, chunk, action):
        byte_array_chunk = bytearray(chunk)
        for index, byte in enumerate(byte_array_chunk):
            salt = ord(self.secret[index % len(self.secret)])
            processed_byte = action(byte, salt) % 256
            byte_array_chunk[index] = processed_byte
        return byte_array_chunk
