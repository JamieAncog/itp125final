import hashlib
import time
import multiprocessing

# Open hashes.txt and read each hash into a list

hash_file = open("hashes.txt", "r")
content = hash_file.read()
hash_file.close()
hashes_list = content.splitlines()

# Use the hashlib library to generate the md5 hash for a given password


def gen_md5(password):
    md5hash = hashlib.md5(password.encode()).hexdigest()
    return md5hash


def all_combos_rec(letters, n, prefixes, prefix, curr_hash, password_list, hashes):
    if len(prefix) == n:
        prefixes.append(prefix)
        if gen_md5(prefix) == hashes[curr_hash]:
            password_list.append(prefix)
            return
    else:
        for x in range(len(letters)):
            all_combos_rec(letters, n, prefixes, prefix + letters[x], curr_hash, password_list, hashes)


def all_combos(letters, n, prefixes, prefix):
    if len(prefix) == n:
        prefixes.append(prefix)
        return
    else:
        for x in range(len(letters)):
            all_combos(letters, n, prefixes, prefix + letters[x])


def decrypt_md5(max_length, curr_hash, password_list, hashes):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@!?"

    length = 1
    while length <= max_length:
        prefixes = []
        all_combos_rec(chars, length, prefixes, "", curr_hash, password_list, hashes)
        # print(prefixes)
        if len(password_list) > 0 and gen_md5(password_list[-1]) == hashes[curr_hash]:
            return
        length += 1


def helper(n):
    passwords = []
    passwords_file = open("passwords.txt", "a")
    start_time = time.perf_counter()

    decrypt_md5(5, n, passwords, hashes_list)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(passwords[-1])
    print(str(elapsed_time) + " seconds to crack\n\n")

    passwords_file.close()

'''
if __name__ == '__main__':
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=helper, args=(i,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

'''


def do_sm():
    print("Sleeping 1 second...")
    time.sleep(1)
    print("Done Sleeping...")


def h():
    my_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@!?"
    my_prefixes = []
    all_combos(my_chars, 8, my_prefixes, "")


if __name__ == '__main__':
    st = time.perf_counter()

    processes = []
    for i in range(1):
        p = multiprocessing.Process(target=h)
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    en = time.perf_counter()
    ela = en - st
    print(str(ela) + " seconds")
