

def thay_the_tu(sentence, replacements):
    new_sentence = sentence

    for key, values in replacements.items():
        for value in sorted(values, key=lambda x: -x[1]):
            value_text, start_index, end_index = value
            new_sentence = new_sentence[:start_index] + key[0] + new_sentence[end_index+1:]

    return new_sentence

# Ví dụ
# sentence = "Tiến là lập trình viên, Anh ấy rất giỏi."
# replacements = {('Tiến', 0, 3): [('lập trình viên', 8, 21), ('Anh ấy', 24, 29)]}

# new_sentence = thay_the_tu(sentence, replacements)
# print(new_sentence)
