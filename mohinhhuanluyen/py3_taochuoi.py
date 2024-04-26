

def chuyen_hoa_chuoi(pairs):
  rs = [];
  for pair in pairs:
    lf,rt = pair;
    tmpRS="";
    ct,tt,st,end = lf;
    tmpRS += ct + "/" + tt + "/" + str(st) + "/" + str(end);
    ct,tt,st,end = rt;
    tmpRS += " - " + ct + "/" + tt + "/" + str(st) + "/" + str(end);
    rs.append(tmpRS);
  return rs;