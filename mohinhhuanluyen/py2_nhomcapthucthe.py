

def nhom_cap_thuc_the(capthucthe):
  pairs = []
  if capthucthe:
    for i in range(len(capthucthe)):
      for j in range(i+1,len(capthucthe)):
        pairs.append((capthucthe[i], capthucthe[j]));
  return pairs