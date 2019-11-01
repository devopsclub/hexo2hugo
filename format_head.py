import os


def format_head(file_path):
    cur_dir, file_name = os.path.split(file_path)
    new_dir = os.path.join(cur_dir, "converted")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        format_tags_categories(lines)
        format_time(lines)

    with open(os.path.join(new_dir, file_name), "w", encoding="utf-8") as nf:
        for i in lines:
            nf.write(i)


def format_tags_categories(lines):
    begin_index  = 0
    end_index = 0
    tags_index = 0
    categories_index = 0
    tags = []
    categories = []
    for i in range(len(lines)):
        if "---" in lines[i]:
            begin_index = i
        if begin_index and not end_index and "---" in lines[i]:
            end_index = i
        if "tags" in lines[i]:
            tags_index = i
            lines[i] = ""
        if "categories" in lines[i]:
            categories_index = i
            lines[i] = ""
    if not categories_index:
        categories_index = end_index
    for i in range(tags_index, categories_index):
        if "-" in lines[i]:
            tags.append(lines[i].strip(" ").strip("\t").strip("-").strip())
            lines[i] = ""
    for i in range(categories_index, end_index):
        if "-" in lines[i]:
            categories.append(lines[i].strip(" ").strip("\t").strip("-").strip())
            lines[i] = ""
    lines.insert(end_index, "categories: " + str(categories) + "\n")
    lines.insert(end_index, "tags: " + str(tags) + "\n")


def format_time(lines):
    time_index = 0
    for i in range(len(lines)):
        if "date:" in lines[i]:
            time_index = i
    time_list = lines[time_index].split(" ")
    result = time_list[0] + " " + time_list[1] + "T" + time_list[2].strip() + "+08:00\n"
    lines[time_index] = result


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "post")
    for i in os.listdir(file_path):
        if os.path.isfile(os.path.join(file_path, i)) and ".md" in i:
            format_head(os.path.join(file_path, i))