import hashlib
import time
import multiprocessing
from numba import jit, cuda

# Open hashes.txt and read each hash into a list

hash_file = open("hashes.txt", "r")
content = hash_file.read()
hash_file.close()
hashes_list = content.splitlines()

# Use the hashlib library to generate the md5 hash for a given password

# @jit(target_backend='cuda')


def gen_md5(password):
    md5hash = hashlib.md5(password.encode()).hexdigest()
    return md5hash


def all_combos(letters, n, prefixes, prefix):
    if len(prefix) == n:
        prefixes.append(prefix)
        return
    else:
        for x in range(len(letters)):
            all_combos(letters, n, prefixes, prefix + letters[x])


def decrypt_md5(max_length, curr_hash, password_list, hashes):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    length = 1
    while length <= max_length:
        prefixes = []
        all_combos(chars, length, prefixes, "")
        for prefix in prefixes:
            if gen_md5(prefix) == hashes[curr_hash]:
                password_list.append(prefix)
                return
        length += 1


def helper(password_list, max_length, index, hashes):
    passwords_file = open("passwords.txt", "a")
    start_time = time.perf_counter()

    decrypt_md5(max_length, index, password_list, hashes)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(password_list[-1])
    print(str(elapsed_time) + " seconds to crack\n")

    passwords_file.write(password_list[-1] + "\n")
    passwords_file.write(str(elapsed_time) + " seconds to crack\n\n")
    passwords_file.close()


if __name__ == '__main__':

    st = time.perf_counter()

    passwords = []
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=helper, args=(passwords, 4, i, hashes_list))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    en = time.perf_counter()
    ela = en - st
    print(str(ela) + " seconds")
