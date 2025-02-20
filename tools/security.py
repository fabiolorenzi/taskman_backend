from random import randint

def generatePasscode(user_id):
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    all_values = list(lowercase) + list(uppercase) + list(numbers)

    result = str(user_id)

    while len(result) < 50:
        result += all_values[randint(0, len(all_values) - 1)]
    return result