
from sentence_transformers import SentenceTransformer
import json
import numpy as np
import csv
import os
from py1_tachthucthe import xulyngoac, tach_thuc_the
from py2_nhomcapthucthe import nhom_cap_thuc_the
from py3_taochuoi import chuyen_hoa_chuoi
from py4_docfiledulieu import get_data_train_vecto_csv
from py5_taokeyvalue import nhomcapthucthe
from py6_gopcackey import process_data
from py7_xoavalue import remove_duplicates
from py8_xoakey import remove_subset_keys
from py9_thaythechuoi import thay_the_tu
from py10_taoSVM import model_svm

model = SentenceTransformer('keepitreal/vietnamese-sbert')

def dict_to_custom_string(d):
    result = "{"
    for key, value in d.items():
        if isinstance(value, list) and len(value) > 0:
            value_strings = [str(v[0]) for v in value]
            result += "'" + str(key) + "': " + str(value_strings) + ", "
    result = result.rstrip(", ") + "}"
    return result

def dong_tham_chieu(cau,svm_model=model_svm()):
    cau = xulyngoac(cau)
    thuctheTrain = tach_thuc_the(cau,1)
    # print("1: ",thuctheTrain)
    thuctheThamChieu = nhom_cap_thuc_the(tach_thuc_the(cau,2))

    thucthetrave = tach_thuc_the(cau,0)

    thucthenhomcap = nhom_cap_thuc_the(thucthetrave)
    # print("2: ",thuctheThamChieu)

    nhom_cap = nhom_cap_thuc_the(thuctheTrain)

    chuoithucthe = chuyen_hoa_chuoi(nhom_cap)
    # print("3: ",chuoithucthe)

    vectoThucThe = []

    for chuoi in chuoithucthe:
        embeddings = model.encode(chuoi)
        vectoThucThe.append(embeddings);

    # print("len 1: ",len(vectoThucThe))

    output_file_path = "tmp_vecto.csv"
    with open(output_file_path, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for vector in vectoThucThe:
            writer.writerow(np.array(vector))

    vectoThucThe = get_data_train_vecto_csv(output_file_path)
    # print("len 2: ",len(vectoThucThe))
    # print("vecto 2: ",vectoThucThe[0])

    os.remove(output_file_path)

    # print("4: ",len(vectoThucThe))

    capdongthamchieu = []
    if len(vectoThucThe) > 0:

        ketqua = svm_model.predict(vectoThucThe)

        # print("5: ",ketqua)

        ketquadongthamchieu = []
        for index, kq in enumerate(ketqua):
            chuoi = str(thucthenhomcap[index])+" "+str(kq)
            ketquadongthamchieu.append(chuoi)

        # print(ketquadongthamchieu)

        for index, kq in enumerate(ketqua):
            if kq:
                capdongthamchieu.append(thuctheThamChieu[index])

        # print("6: ",capdongthamchieu)

        nhomcap = nhomcapthucthe(capdongthamchieu)

        lamphang = process_data(nhomcap)

        xoaTTgiong = remove_duplicates(lamphang)

        caphoanchinh = remove_subset_keys(xoaTTgiong)

        # print("7: ",nhomcap)
        # print("8: ",lamphang)
        # print("9: ",xoaTTgiong)
        # print("10: ",caphoanchinh)

        rs = thay_the_tu(xulyngoac(cau),caphoanchinh)

        result = {
            "caucuoi": rs,
            "capthaythe": dict_to_custom_string(caphoanchinh),
            "ketquadongthamchieu": ketquadongthamchieu,
            "danhsachthucthe": thucthetrave
        }
        json_result = json.dumps(result, ensure_ascii=False)

    return json_result
# svm_model = model_svm();
# data = [
#     'Năm nay, Tiến sẽ tốt nghiệp ĐẠI HỌC. Anh ấy sẽ trở thành 1 kỹ sư.',
#     'Hồng Trần Nữ là nữ diễn viên hạng a. Giải thưởng nữ diễn viên suất sắc năm nay thuộc về cô ấy.',
#     'Tiến và tiên là đôi bạn thân. Hai người họ quen biết đã lâu.', # chưa chuẩn
#     'Lớp trưởng nay không đi học. Cô ấy bị ốm nặng.'
#     ]
# data = "Hồng Trần Nữ là nữ diễn viên hạng a. Giải thưởng nữ diễn viên suất sắc năm nay thuộc về cô ấy."
# rs = dong_tham_chieu(data,svm_model)
# print(rs)