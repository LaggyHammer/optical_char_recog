from fuzzysearch import find_near_matches
import itertools
import re


# Remove Formatting
def formatting(result_list):
    results = []
    for value in result_list:
        if value != ' ':
            for m in itertools.islice(re.finditer("\d{1,7}[^a-np-z](\.|,){0,1}(\d|o){0,3}", value), 1):
                # Regex: 1-5 digits with decimal
                result = m.string[m.start():m.end()]
                # print(result)
                results.append(result)
        else:
            results.append(value)

    return results


def regular_exp(unit):
    mapping = {'kg': "\d{1,5}(\.|,){0,1}(\d|o){0,3}\s{0,1}k(g|o|9)",
               'kg/mm': "\d{0,3}(\.|,){0,1}(\d|o){0,3}\s{0,1}k(g|o|9)\/mm",
               'rpm or equivalent': "\d{2,5}\s{0,1}(r.{0,1}\s{0,1}p.{0,1}\s{0,1}m.{0,1}|r\s{0,1}\/\s{0,1}min){0,1}"}
    try:
        reg_exp = mapping[unit]

    except KeyError:
        print('Unit not available')
        reg_exp = ' '

    return reg_exp


def search_function(text, key, details):
    regex = regular_exp(details['Unit(s)'])

    # search main key
    text = text.lower()
    results = []
    key = key.lower()
    match_list = find_near_matches(key, text, max_l_dist=2)
    # print(match_list)  # debug
    for match in match_list:
        search_start = match.start
        search_string = text[search_start:]
        for m in itertools.islice(re.finditer(regex, search_string), int(details['Occurrence(s)'])):
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    if not bool(results):
        for alternate in details['Alternate(s)']:
            results = []
            key = alternate.lower()
            match_list = find_near_matches(key, text, max_l_dist=2)
            # print(match_list)  # debug
            for match in match_list:
                search_start = match.start
                search_string = text[search_start:]
                for m in itertools.islice(re.finditer(regex, search_string), int(details['Occurrence(s)'])):
                    result = m.string[m.start():m.end()]
                    # print(result)
                    results.append(result)

                if bool(results):
                    break

    if len(results) < int(details['Occurrence(s)']):
        results = results + ([' '] * int(details['Occurrence(s)']))

    return results
