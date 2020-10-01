# This code is written by Nicky Ru

from encryptor import encrypt

if __name__ == '__main__':
    message = input("Enter your message: ")  # e.g. 0123456789ABCDEF
    key = input("Enter your key: ")  # e.g. 133457799BBCDFF1
    result = encrypt(message, key)
    print("Your encrypted message is:", result.upper())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
