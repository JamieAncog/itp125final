import hashlib
import time
import multiprocessing

# Open hashes.txt and read each hash into a list

hash_file = open("hashes.txt", "r")
content = hash_file.read()
hash_file.close()
hashes_list = content.splitlines()

# This function uses the hashlib module to generate the md5 hash for a given password


def gen_md5(password):
    md5hash = hashlib.md5(password.encode()).hexdigest()
    return md5hash


# This function generates all possible combinations of a string at a given length


def all_combos(letters, n, prefixes, prefix):
    if len(prefix) == n:
        prefixes.append(prefix)
        return
    else:
        for x in range(len(letters)):
            all_combos(letters, n, prefixes, prefix + letters[x])


# This function decrypts the hash at a given index and adds it to a list of passwords


def crack_md5(max_length, index, password_list, hashes):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@!?"

    # At each possible length, find every possible combination of characters and add to combos list
    # Iterate through each combination and check for a password match

    length = 1
    while length <= max_length:
        combos = []
        all_combos(chars, length, combos, "")
        for combo in combos:
            if gen_md5(combo) == hashes[index]:
                password_list.append(combo)
                return
        length += 1


# This function decrypts each hash using a timer and writes the password to the passwords.txt


def helper(password_list, max_length, index, hashes):

    # Open passwords.txt in append mode

    passwords_file = open("passwords.txt", "a")

    # Start a timer using the time module

    start_time = time.perf_counter()

    # Use the decrypt function to find the hash at a given index

    crack_md5(max_length, index, password_list, hashes)

    # End the timer and calculate the elapsed time

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # Output the passwords and time to crack to the screen

    print(password_list[-1] + "\t" + str(elapsed_time) + " seconds to crack")

    # Record the password in passwords.txt along with the time taken to crack

    passwords_file.write(password_list[-1] + "\n")
    passwords_file.write(str(elapsed_time) + " seconds to crack\n\n")
    passwords_file.close()


if __name__ == '__main__':

    # Use multiple processing cores to decrypt each password

    passwords = []
    processes = []
    for i in range(len(hashes_list)):

        # Create a process and store in a list. Start the process

        p = multiprocessing.Process(target=helper, args=(passwords, 8, i, hashes_list))
        processes.append(p)
        p.start()

    # Stop the execution of the main program until all processes are complete

    for process in processes:
        process.join()
