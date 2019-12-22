from fuzzysearch import find_near_matches
import itertools
import re


# Static Load Function
def find_static_load(text, key='STATIC LOAD PER SUPPORT POINT'):
    results = []
    key = key.lower()
    match_list = find_near_matches(key, text, max_l_dist=2)
    for match in match_list:
        search_start = match[0]
        search_string = text[search_start:]
        equal_sign_pos = search_string.find('=')
        search_string = search_string[equal_sign_pos - 5: equal_sign_pos + 100]
        for m in itertools.islice(re.finditer("p.{0,2}s{0,1}\s{0,1}=\s{0,1}\d{1,5}(\.|,){0,1}(\d|o){0,3}\s{0,1}k(g|o|9)",
                                              search_string), 2):
            # Regex: 'p + 0-2 characters + s (maybe) + space (maybe) + = + 1-5 digits + . or , (maybe) + 0-3 digits or
            # 'o's + space (maybe) + k + g or o
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    return results


# Spring Constant Function
def find_spring_constant(text, key='SPRING CONSTANT OF'):
    results = []
    key = key.lower()
    match_list = find_near_matches(key, text, max_l_dist=2)
    for match in match_list:
        search_start = match[0]
        search_string = text[search_start:]
        for m in itertools.islice(re.finditer("\d{0,3}(\.|,){0,1}(\d|o){0,3}\s{0,1}k(g|o|9)\/mm", search_string), 1):
            # Regex: 0-3 digits + . or , (maybe) + 0-3 digits or 'o's + space (maybe) + k + g or o + /mm
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    return results


# Operating Speed Function
def find_operating_speed(text, key='OPERATING SPEED'):
    results = []
    key = key.lower()
    match_list = find_near_matches(key, text, max_l_dist=2)
    for match in match_list:
        search_start = match[0]
        search_string = text[search_start:]
        for m in itertools.islice(
                re.finditer("\d{1,5}\s{0,1}(r.{0,1}\s{0,1}p.{0,1}\s{0,1}m.{0,1}|r\s{0,1}\/\s{0,1}min){0,1}", search_string),
                1):
            # Regex: 1-5 digits + space (maybe) + (rpm or r.p.m. or r/min)
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    return results


# Total Mass Function
def find_total_mass(text, key='TOTAL MASS OF'):
    results = []
    key = key.lower()
    match_list = find_near_matches(key, text, max_l_dist=2)
    for match in match_list:
        search_start = match[0]
        search_string = text[search_start:]
        equal_sign_pos = search_string.find('=')
        search_string = search_string[equal_sign_pos - 5: equal_sign_pos + 100]
        for m in itertools.islice(re.finditer("\d{1,5}\s{0,1}k(g|o|9)", search_string), 1):
            # Regex: 1-5 digits + space (maybe) + k + g or o
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    return results


# Dynamic Loads Function
def find_dynamic_loads(text, key='DYNAMIC'):
    results = []
    key = key.lower()
    match_list = find_near_matches('total mass of', text, max_l_dist=2)
    text = text[match_list[0][0]:]
    match_list = find_near_matches(key, text, max_l_dist=2)
    for match in match_list:
        search_start = match[0]
        search_string = text[search_start:]
        next_field_pos = search_string.find('spring')
        search_string = search_string[: next_field_pos]
        for m in itertools.islice(re.finditer("\d{0,5}(\.|,){0,1}(\d|o){0,3}\s{0,1}k(g|o|9)", search_string), 10):
            # Regex: 0-5 digits + . or , (maybe) + 0-3 digits or 'o's + space (maybe) + k + g or o
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    return results
