import string

# Method from: https://en.wikipedia.org/wiki/International_Bank_Account_Number#Algorithms

# Replace each letter in the string with two digits, thereby expanding the string, where A = 10, B = 11, ..., Z = 35
LETTERS = {ord(d): str(i) for i, d in enumerate(string.digits + string.ascii_uppercase)}


# Move the four initial characters to the end of the string, and replacing the dictionary values
def process_iban(iban):
    return (iban[4:] + iban[:4]).translate(LETTERS)


# Interpret the string as a decimal integer and compute the remainder of that number on division by 97
def verify_iban(iban):
    return int(process_iban(iban)) % 97 == 1
