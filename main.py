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


def all_combos(letters, n, prefixes, prefix):
    if len(prefix) == n:
        print(prefix)
        prefixes.append(prefix)
        return
    else:
        for x in range(len(letters)):
            all_combos(letters, n, prefixes, prefix + letters[x])


def decrypt_md5(max_length, curr_hash, password_list, hashes):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    chars_with_symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*()?"

    length = 1
    while length <= max_length:
        prefixes = []
        all_combos(chars, length, prefixes, "")
        for prefix in prefixes:
            if gen_md5(prefix) == hashes[curr_hash]:
                password_list.append(prefix)
                return
        length += 1


passwords = []
for i in range(1):
    passwords_file = open("passwords.txt", "a")
    start_time = time.perf_counter()

    decrypt_md5(10, 4, passwords, hashes_list)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(passwords[-1])
    print(str(elapsed_time) + " seconds to crack\n")

    passwords_file.write(passwords[-1] + "\n")
    passwords_file.write(str(elapsed_time) + " seconds to crack\n\n")
    passwords_file.close()


hash_file.close()