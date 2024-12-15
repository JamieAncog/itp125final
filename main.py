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


def all_combos(start, letters, n, prefixes, prefix, password_list, hashes):
    if len(prefix) == n:
        prefixes.append(prefix)
        for curr_hash in hashes:
            if gen_md5(prefix) == curr_hash:
                password_list.append(prefix)
                curr_time = time.time()
                elapsed_time = curr_time - start

                passwords_file = open("passwords.txt", "a")
                passwords_file.write(passwords[-1] + "\n")
                passwords_file.write(str(elapsed_time) + " seconds to crack\n\n")
                passwords_file.close()

                del curr_hash
                return
    else:
        for x in range(len(letters)):
            all_combos(start, letters, n, prefixes, prefix + letters[x], password_list, hashes)


def decrypt_md5(max_length, password_list, hashes):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@!?"
    start_time = time.time()

    length = 1
    while length <= max_length and len(hashes) > 0:
        prefixes = []
        all_combos(start_time, chars, length, prefixes, "", password_list, hashes)
        length += 1


passwords = []
decrypt_md5(10, passwords, hashes_list)


hash_file.close()