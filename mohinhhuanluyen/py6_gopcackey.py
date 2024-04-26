
def process_data(data):
    processed_data = data.copy()

    for key, value in data.items():
        for other_key, other_value in data.items():
            if key != other_key and key in other_value:
                processed_data[other_key].extend(value)
                del processed_data[key]
                break

    return processed_data

# data = {
#     ('Tien', 0, 3): [('new car', 19, 25), ('he', 33, 34)],
#     ('new car', 19, 25): [('he', 33, 34)]
# }

# processed_data = process_data(data)

# print(processed_data)