import csv
import re


def open_file():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def compile_new_list(contacts_list=None):
    if contacts_list is None:
        contacts_list = open_file()
    new_list = []

    for i in contacts_list:
        temp_list = []

        if len(i[0].split()) == 1:
            temp_list.append(i[0])
        if len(i[1].split()) == 1:
            temp_list.append(i[1])
        if len(i[2].split()) == 1:
            temp_list.append(i[2])
        else:
            if len(i[0].split()) > 1:
                for it in re.split(' ', i[0]):
                    temp_list.append(it)
            if len(i[1].split()) > 1:
                firstname = re.split(' ', i[1])
                for it in firstname:
                    temp_list.append(it)
        if len(temp_list) == 2:
            temp_list.append('')

        temp_list.append(i[3])
        temp_list.append(i[4])

        if "доб" in i[5]:
            pattern = re.compile(r"(^(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})["
                                 r"\s-]*(\d{2})[\s-]*(\d+)\s\(?([а-я.]+)\s?("
                                 r"\d{4})\)?)")
            result = pattern.sub("+7(\\3)\\4-\\5-\\6 \\7\\8", i[5])
        else:
            pattern = re.compile(r"(^(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})["
                                 r"\s-]*(\d{2})[\s-]*(\d+))")
            result = pattern.sub("+7(\\3)\\4-\\5-\\6", i[5])

        temp_list.append(result)
        temp_list.append(i[6])
        new_list.append(temp_list)
    return new_list


def merge_strings(new_list=None):
    if new_list is None:
        new_list = compile_new_list()
    result_list = []
    for i in new_list:
        flag_names = True
        if len(result_list) != 0:
            for it in result_list:
                if i[0] == it[0] and i[1] == it[1]:
                    for n in range(2, 7):
                        if len(it[n]) == 0:
                            it[n] = i[n]
                    flag_names = False
                    break
        else:
            result_list.append(i)
            flag_names = False
        if flag_names:
            result_list.append(i)
    return result_list


def write_new_file(result_list=None):
    if result_list is None:
        result_list = merge_strings()
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result_list)


if __name__ == '__main__':
    write_new_file()
