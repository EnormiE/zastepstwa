import re

def indent(string):
    counter = '\n\t'
    new_string = ''
    start = 0
    for match in re.finditer(r'({|}, )', string):
        end, new_start = match.span()
        new_string += string[start:end]
        if match.group(0) == '}, ':
            counter = counter[:-2]
        rep = match.group(0) + str(counter)
        new_string += rep
        start = new_start
        counter += '\t'
    new_string += string[start:]
    return new_string

diff = str({'values_changed': {"root['08.09.2023 piątek']['9']['opis']": {'new_value': '2 RP - Uczniowie zwolnieni do domu', 'old_value': '2 RP(1) - Język angielski, 301'}, "root['08.09.2023 piątek']['9']['zastepca']": {'new_value': '', 'old_value': 'Agnieszka Pylak'}}})

diff = indent(diff)

print(diff)

# import re
#
# def indent(string):
#     counter = '\n\t'
#     new_string = ''
#     start = 0
#     for match in re.finditer(r'({|}, )', string):
#         end, new_start = match.span()
#         new_string += string[start:end]
#         if match.group(0) == '}, ':
#             counter = counter[:-2]
#         rep = match.group(0) + str(counter)
#         new_string += rep
#         start = new_start
#         counter += '\t'
#     new_string += string[start:]
#     string_1 = new_string
#     print(string_1)
#     new_string = ''
#     start = 0
#     for match in re.finditer(r'}', string_1):
#         end, new_start = match.span()
#         new_string += string_1[start:end]
#         # print(string_1[168:170])
#         # print(string_1[end: new_start + 1])
#         if string_1[end: new_start + 1] == '},':
#             rep = str(counter) + match.group(0)
#         elif string_1[end - 1: new_start] == "'}":
#             rep = str(counter) + match.group(0) + str(counter)
#         else:
#             rep = match.group(0) + str(counter)
#         new_string += rep
#         start = new_start
#         counter = counter[:-1]
#     new_string += string_1[start:]
#     return new_string
#
# diff = str({'values_changed': {"root['08.09.2023 piątek']['9']['opis']": {'new_value': '2 RP - Uczniowie zwolnieni do domu', 'old_value': '2 RP(1) - Język angielski, 301'}, "root['08.09.2023 piątek']['9']['zastepca']": {'new_value': '', 'old_value': 'Agnieszka Pylak'}}})
#
# diff = indent(diff)
#
# print(diff)