
def remove_duplicates(data):
    # Tạo một bản sao của data để tránh sửa đổi trực tiếp
    processed_data = data.copy()

    # Duyệt qua từng key trong data
    for key, value in data.items():
        # Loại bỏ các giá trị trùng nhau trong mỗi key bằng cách chuyển value thành một set
        processed_data[key] = list(set(value))

    return processed_data

# data = {('Tiến và Tiên', 0, 11): [('Họ', 30, 31),('Họ', 30, 31)], ('bạn thân', 20, 27): [('Họ', 30, 31)]}

# # Loại bỏ các giá trị trùng nhau
# processed_data = remove_duplicates(data)

# # In ra kết quả
# print(processed_data)