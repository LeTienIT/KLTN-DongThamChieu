

def nhomcapthucthe(arr):
  result_dict = {}
  for item in arr:
      key1, key2 = item[0], item[1]
      if key1 in result_dict:
          result_dict[key1].append(key2)
      else:
          result_dict[key1] = [key2]
  return result_dict

# arr = [
#         (('Tien', 0, 3), ('new car', 19, 25)),
#         (('Tien', 0, 3), ('he', 33, 34)),
#         (('new car', 19, 25), ('he', 33, 34))
#       ]
# tmp = nhomcapthucthe(arr)
# print(tmp)