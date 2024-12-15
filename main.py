import hashlib
import time

# Open hashes.txt and read each hash into a list

hash_file = open("hashes.txt", "r")
content = hash_file.read()
hashes_list = content.splitlines()

# Use the hashlib library to generate the md5 hash for a given password


def gen_md5(password):
    md5hash = hashlib.md5(password.encode()).hexdigest()
    return md5hash


def find_password(attempts, max_length, curr_hash, password_list, hashes):

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    chars_with_symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*()?"

    first_try = crack_hash(chars, attempts, max_length, curr_hash, password_list, hashes)

    if not first_try:
        try_again = crack_hash(chars_with_symbols, attempts, max_length, curr_hash, password_list, hashes)
        if not try_again:
            password_list.append("Could not crack")


def crack_hash(char_list, attempts, max_length, curr_hash, password_list, hashes):
    is_cracked = False
    while len(attempts[-1]) <= max_length and not is_cracked:
        is_cracked = try_next(char_list, attempts, curr_hash, password_list, hashes)
    if is_cracked:
        return True
    else:
        return False


def try_next(char_list, attempts, curr_hash, password_list, hashes):
    curr = attempts[0]
    for curr_char in char_list:
        print(curr + curr_char)
        if gen_md5(curr + curr_char) == hashes[curr_hash]:
            password_list.append(curr + curr_char)
            return True
        else:
            attempts.append(curr + curr_char)
    del attempts[0]
    return False


passwords = []
for i in range(len(hashes_list)):
    passwords_file = open("passwords.txt", "a")
    start_time = time.perf_counter()

    num_chars = 10
    tries = [""]
    find_password(tries, num_chars, i, passwords, hashes_list)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    passwords_file.write(passwords[-1] + "\n")
    passwords_file.write(str(elapsed_time) + " seconds to crack\n\n")
    passwords_file.close()


hash_file.close()