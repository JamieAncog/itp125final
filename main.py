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


def find_password(attempts, max_length, curr_hash, password_list, hashes):

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@!?"

    crack_hash(chars, attempts, max_length, curr_hash, password_list, hashes)


def crack_hash(char_list, attempts, max_length, curr_hash, password_list, hashes):
    is_cracked = [False]
    my_processes = []
    while len(attempts[-1]) <= max_length and not is_cracked[0]:
        p1 = multiprocessing.Process(target=try_next, args=(char_list, attempts, curr_hash, password_list, hashes,
                                                           is_cracked))
        my_processes.append(p1)
        p1.start()

    for my_p in my_processes:
        my_p.join()


def try_next(char_list, attempts, curr_hash, password_list, hashes, cracked):
    curr = attempts[0]
    for curr_char in char_list:
        # print(curr + curr_char)
        if gen_md5(curr + curr_char) == hashes[curr_hash]:
            password_list.append(curr + curr_char)
            cracked[0] = True
            return
        else:
            attempts.append(curr + curr_char)
    del attempts[0]


def helper(ml, n):
    passwords = []
    passwords_file = open("passwords.txt", "a")
    start_time = time.perf_counter()

    tries = [""]
    find_password(tries, ml, n, passwords, hashes_list)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if len(passwords) > 0:
        print(passwords[-1])
    print(passwords)
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


if __name__ == '__main__':

    s = time.perf_counter()

    helper(1, 0)
    helper(2, 1)

    e = time.perf_counter()
    el = e - s
    print(str(el) + " seconds")

    st = time.perf_counter()

    processes = []
    for i in range(2):
        p = multiprocessing.Process(target=helper, args=(i+1, i))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    en = time.perf_counter()
    ela = en - st
    print(str(el) + " seconds")
    print(str(ela) + " seconds")

