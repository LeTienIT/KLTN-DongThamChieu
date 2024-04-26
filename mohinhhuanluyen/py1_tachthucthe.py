import spacy
import re
nlp = spacy.load('vi_core_news_lg')

arrNot = [",",".",'tên','là',"ngồi","bài","bị","nói","đến","để","đành","trong","chuyến","cho","ở"
          ,"thưởng_thức","hiện","nhiều","chắc","đó","cũ","vì","giỏi","thấy","ngoài","gì","nay"]
arrTrue = ["P","CC","V","N","Np","Nc","A","M"]

textNot = ["ccomp","ROOT","xcomp"]
textTrue = ["người","món","cá"]

def xulyngoac(string):
    if string[-1] != '.':
        string += '.'
    tmp0 = string.replace('-', ' - ')
    tmp1 = tmp0.replace('(', '( ')
    tmp2 = tmp1.replace(')', ' )')
    tmp3 = tmp2.replace('[', '[ ')
    tmp4 = tmp3.replace(']', ' ]')
    return tmp4

def vi_tri_danh_tu(main_string, substring, start_position):
    start_index = main_string.find(substring, start_position)
    if start_index == -1:
        return None
    end_index = start_index + len(substring) - 1
    return start_index, end_index;

def find_word_not(word, word_array=arrNot):
    return word not in word_array

def find_word_true(word, word_array=arrTrue):
    return word in word_array

def find_text_true(word, word_array=textTrue):
    return word.strip().lower() in word_array

def find_text_not(word, word_array=textNot):
    return word not in word_array

def remove_underscores(string):
    return string.replace('_', ' ')

def tach_thuc_the(sentence,original):
    kq = []
    doc = nlp(sentence)
    i = 0;  vitricat = 0
    capthucthe = []
    while i < len(doc) - 1:
      # print("doc[i].text: ",doc[i].text)

      if doc[i].tag_ == "Np" :
        chuoiTMP = ""
        while (doc[i].tag_ == "Np" or doc[i].tag_ == "CC" or doc[i].tag_ == "N") and find_word_not(doc[i].text.strip().lower()):
          if doc[i].text.strip().lower() == "và":
            if (i < len(doc) - 2) and (doc[i+1].tag_ == "Np" or doc[i+1].tag_ == "N" or doc[i+1].tag_ == "P"):
              chuoiTMP += doc[i].text+" "
              i+=1
            else:
              i+=1;
              break;
          elif (i < len(doc) - 2) and (doc[i].tag_ == "N" and ( doc[i+1].tag_ == "A" and find_text_not(doc[i+1].dep_) )) and find_word_not(doc[i].text.strip().lower()):
            chuoiTMP += doc[i].text +" "+doc[i+1].text+" "
            i+=2
            break;
          elif (i < len(doc) - 2) and (doc[i].tag_ == "N" and ( doc[i+1].tag_ == "A" and (not find_text_not(doc[i+1].dep_)) )) and find_word_not(doc[i].text.strip().lower()):
            chuoiTMP += doc[i].text+" "
            i+=2
            break;
          elif doc[i].tag_ == "V" and ( find_text_not(doc[i].dep) or find_text_true(doc[i-1].text) ) and find_word_not(doc[i].text.strip().lower()):
            if (i < len(doc) - 2) and ((doc[i+1].tag_ == "N" or doc[i+1].tag_ == "P") and doc[i-1].tag_ != "Np"):
              chuoiTMP += doc[i].text+" "
              i+=1
            else:
              i+=1;
              break;
          else:
            chuoiTMP += doc[i].text+" "
            i+=1;

        if chuoiTMP!="":
          chuoichuan = remove_underscores(chuoiTMP);
          chuoiTMP = chuoichuan.strip()

          vi_tri_chuoi = vi_tri_danh_tu(sentence,chuoiTMP,vitricat);

          vitricat = vi_tri_chuoi[1];
          if original == 1:
            capthucthe.append((sentence,chuoiTMP,vi_tri_chuoi[0],vi_tri_chuoi[1]))
          elif original == 2:
            capthucthe.append((chuoiTMP,vi_tri_chuoi[0],vi_tri_chuoi[1]))
          else:
            capthucthe.append(chuoiTMP)
        else:
          i+=1

      elif doc[i].tag_ == "N" or doc[i].tag_ == "P" :
        chuoiTMP = ""
        while find_word_true(doc[i].tag_) and find_word_not(doc[i].text.strip().lower()):
          if (i < len(doc) - 2) and (doc[i].tag_ == "N" and ( doc[i+1].tag_ == "A" and find_text_not(doc[i+1].dep_) )) and find_word_not(doc[i].text.strip().lower()):
            chuoiTMP += " "+doc[i].text +" "+doc[i+1].text
            i+=2
            break;
          elif (i < len(doc) - 2) and (doc[i].tag_ == "N" and doc[i+1].tag_ == "Z") and find_word_not(doc[i].text.strip().lower()):
            chuoiTMP += " "+doc[i].text +" "+doc[i+1].text
            i+=2
            break;
          elif (i < len(doc) - 2) and (doc[i].tag_ == "N" and ( doc[i+1].tag_ == "A" and (not find_text_not(doc[i+1].dep_)) )) and find_word_not(doc[i].text.strip().lower()):
            chuoiTMP += " "+doc[i].text
            i+=2
            break;
          elif (i < len(doc) - 2) and (doc[i].tag_ == "P" and doc[i+1].tag_ == "Nc") and find_word_not(doc[i].text.strip().lower()):
            i+=1
            break;

          elif (i < len(doc) - 2) and (doc[i].tag_ == "N" and (doc[i+1].tag_ == "E" and doc[i+1].dep_ == "case")) and (find_word_not(doc[i+1].text.strip().lower())):
            chuoiTMP += " "+doc[i].text+" "+doc[i+1].text
            i+=2
          elif (i < len(doc) - 2) and (doc[i].tag_ == "N" and (doc[i+1].tag_ == "P" and doc[i+1].dep_ == "det")) and (find_word_not(doc[i+1].text.strip().lower())):
            chuoiTMP += " "+doc[i].text+" "+doc[i+1].text
            i+=2
            break;
          elif doc[i].text.strip().lower() == "và":
            if (i < len(doc) - 2) and (doc[i+1].tag_ == "Np" or doc[i+1].tag_ == "N" or doc[i+1].tag_ == "P"):
              chuoiTMP += " "+doc[i].text
              i+=1
            else:
              i+=1;
              break;
          elif doc[i].tag_ == "V" and find_word_not(doc[i].text.strip().lower()):
            if (i < len(doc) - 2) and ( find_text_not(doc[i].dep_) or find_text_true(doc[i-1].text) ) and ( (doc[i+1].tag_ == "N" or doc[i+1].tag_ == "P" or doc[i+1].tag_ == "CC") and doc[i-1].tag_ != "Np" ):
              chuoiTMP += " "+doc[i].text
              # print(chuoiTMP,find_text_not(doc[i].dep_) ,find_text_true(doc[i-1].text))
              i+=1
            else:
              i+=1;
              break;
          else:
            chuoiTMP += " "+doc[i].text
            i+=1;

        if chuoiTMP!="":
          chuoichuan = remove_underscores(chuoiTMP);
          chuoiTMP = chuoichuan.strip()

          vi_tri_chuoi = vi_tri_danh_tu(sentence,chuoiTMP,vitricat);
          # print("chuoi: ",chuoiTMP," - vi tri: ",vi_tri_chuoi)
          vitricat = vi_tri_chuoi[1];
          if original == 1:
            capthucthe.append((sentence,chuoiTMP,vi_tri_chuoi[0],vi_tri_chuoi[1]))
          elif original == 2:
            capthucthe.append((chuoiTMP,vi_tri_chuoi[0],vi_tri_chuoi[1]))
          else:
            capthucthe.append(chuoiTMP)
        else:
          i+=1

      elif doc[i].tag_ == "Nc" or ( doc[i].tag_ == "R" and doc[i].dep_ == "nsubj" ):
        chuoiTMP = doc[i].text
        while (i < len(doc) - 2) and ( doc[i+1].tag_ == "N" or ( (doc[i+1].tag_ == "A" and find_text_not(doc[i+1].dep_)) and doc[i+1].dep_ != "advmod") or doc[i+1].tag_ == "Np" or (doc[i+1].tag_ == "P" and doc[i+1].dep_ != "nsubj") ) and find_word_not(doc[i].text.strip().lower()):
          # print(doc[i+1].text,doc[i+1].tag_ == "A",doc[i+1].dep_ != "advmod" )
          chuoiTMP +=" "+doc[i+1].text
          i+=1
        i+=1
        if chuoiTMP!="":
          chuoichuan = remove_underscores(chuoiTMP);
          chuoiTMP = chuoichuan.strip()

          vi_tri_chuoi = vi_tri_danh_tu(sentence,chuoiTMP,vitricat);

          # print(chuoiTMP,vi_tri_chuoi)
          vitricat = vi_tri_chuoi[1];
          if original == 1:
            capthucthe.append((sentence,chuoiTMP,vi_tri_chuoi[0],vi_tri_chuoi[1]))
          elif original == 2:
            capthucthe.append((chuoiTMP,vi_tri_chuoi[0],vi_tri_chuoi[1]))
          else:
            capthucthe.append(chuoiTMP)
        else:
          i+=1

      elif (i < len(doc) - 2) and doc[i].tag_ == "M" and doc[i+1].tag_ == "N" and doc[i+2].tag_ == "P":
        chuoiTMP = ""
        chuoiTMP += " "+doc[i].text+" "+doc[i+1].text+" "+doc[i+2].text
        chuoiTMP = chuoiTMP.strip()
        vi_tri_chuoi = vi_tri_danh_tu(sentence,chuoiTMP,vitricat);

        print(chuoiTMP,vi_tri_chuoi)
        vitricat = vi_tri_chuoi[1];
        if original == 1:
          capthucthe.append((sentence,chuoiTMP,vi_tri_chuoi[0],vi_tri_chuoi[1]))
        elif original == 2:
          capthucthe.append((chuoiTMP,vi_tri_chuoi[0],vi_tri_chuoi[1]))
        else:
          capthucthe.append(chuoiTMP)
        i+=3

      else:
        i+=1
    if i == len(doc) - 1 and (doc[-1].tag_ == 'N' or doc[-1].tag_ == 'Np'):
          chuoichuan = remove_underscores(doc[-1].text.strip());
          chuoiTMP = chuoichuan.strip()
          vi_tri_chuoi = vi_tri_danh_tu(sentence,doc[-1].text.strip(),vitricat);
          vitricat = vi_tri_chuoi[1];
          if original == 1:
            capthucthe.append((sentence,doc[-1].text.strip(),vi_tri_chuoi[0],vi_tri_chuoi[1]))
          elif original == 2:
            capthucthe.append((chuoiTMP,vi_tri_chuoi[0],vi_tri_chuoi[1]))
          else:
            capthucthe.append(chuoiTMP)

    return capthucthe
