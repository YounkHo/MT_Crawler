import csv

CATE_ID_FILE = "data/cate_id.csv"

def get_cate_ids():
    cate_ids = []
    with open(CATE_ID_FILE, "r", encoding="utf-8") as fo:
        reader = csv.reader(fo)
        for item in reader:
            if(reader.line_num == 1):
                continue
            cate_ids.append(item[1])
    return cate_ids

def get_cate_names():
    cate_names = []
    with open(CATE_ID_FILE, "r", encoding="utf-8") as fo:
        reader = csv.reader(fo)
        for item in reader:
            if(reader.line_num == 1):
                continue
            cate_names.append(item[2])
    return cate_names

def get_cate_dict():
    cate_dict = {}
    with open(CATE_ID_FILE, "r", encoding="utf-8") as fo:
        reader = csv.reader(fo)
        for item in reader:
            if(reader.line_num == 1):
                continue
            cate_dict[item[1]] = item[2]
    return cate_dict

def get_cate_name_by_id(cate_id):
    cate_dict = get_cate_dict()
    return cate_dict[cate_id]

# if __name__ == "__main__":
#     print(get_cate_dict())