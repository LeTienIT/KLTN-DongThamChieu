
def remove_subset_keys(dictionary):
    keys_to_remove = []

    # Tạo một bản sao của keys của từ điển để tránh thay đổi kích thước của từ điển trong khi vẫn đang duyệt
    keys_copy = list(dictionary.keys())

    for i, key1 in enumerate(keys_copy):
        values1 = dictionary[key1]
        for key2 in keys_copy[i+1:]:
            values2 = dictionary[key2]
            if all(value2 in values1 for value2 in values2):
                keys_to_remove.append(key2)

    for key in keys_to_remove:
        del dictionary[key]
    return dictionary

# d = {('Tiến và Tiên', 0, 11): [('Họ', 30, 31)], ('bạn thân', 20, 27): [('Họ', 30, 31)]}

# print(remove_subset_keys(d))
