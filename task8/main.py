from models.cipher import Cipher
from models.coder import Private


def input_password():
    while True:
        password = input("Enter password")
        if password:
            return password


if __name__ == '__main__':

    cipher = Cipher()

    secret = input_password()
    pr = Private(secret)

    in_file = '1.png'
    out_file = in_file + cipher.extension
    cipher.cipher(in_file, out_file, pr.encoder)

    in_file, out_file = out_file, 'decoded-' + in_file
    cipher.decipher(in_file, out_file, pr.decoder)
