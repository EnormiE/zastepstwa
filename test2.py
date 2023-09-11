import re

def indent(string):
    counter = '\n\t'
    new_string = ''
    start = 0
    clues = [
        "}, 'type_changes'",
        "}, 'values_changed'",
        "}, 'dictionary_item_added'",
        "}, 'dictionary_item_removed'",
        "}, 'iterable_item_added'",
        "}, 'iterable_item_removed'",
        "}, 'attribute_added'",
        "}, 'attribute_removed'",
        "}, 'set_item_added'",
        "}, 'set_item_removed'",
        "}, 'repetition_change'"
    ]
    for match in re.finditer(r'({|}, )', string):
        end, new_start = match.span()
        new_string += string[start:end]
        if match.group(0) == '}, ':
            counter = counter[:-2]
            for clue in clues:
                if string[end: new_start + (len(clue) - 3)] == clue:
                    # print(string[end: new_start + (len(clue) - 3)])
                    counter = counter[:-1]
                    continue
        rep = match.group(0) + str(counter)
        new_string += rep
        start = new_start
        counter += '\t'
    new_string += string[start:]
    return new_string

diff = str({'values_changed': {"root['08.09.2023 piątek']['9']['opis']": {'new_value': '2 RP - Uczniowie zwolnieni do domu', 'old_value': '2 RP(1) - Język angielski, 301'}, "root['08.09.2023 piątek']['9']['zastepca']": {'new_value': '', 'old_value': 'Agnieszka Pylak'}}, 'dictionary_item_added': {"root['11.09.2023 poniedziałek']": {'4': {'opis': '2 RP - Język angielski, 319', 'zastepca': 'Agnieszka Pylak', 'uwagi': ''}}}})



diff = indent(diff)

print(diff)