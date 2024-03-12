import string


def convert_numb_to_letters(numbers):
    number_list = [int(numb) for numb in str(numbers)]
    print(number_list)
    alpha_dict = dict(enumerate(string.ascii_lowercase))
    print(alpha_dict)
    return [alpha_dict[x] for x in number_list]

print(convert_numb_to_letters(1234567890))