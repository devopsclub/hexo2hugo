"""
---
title: "xxxxx"
date: 2019-11-01 22:15
tags:
    - tag1
    - tag2
categories:
    - categories
---
Format like this will be converted to hugo format. U can customize your script on my script.
"""


import argparse
import os
import logging

default_logging_level = logging.WARNING


class Logger(object):
    def __init__(self, name):
        logformat = '(%(name)s): [%(levelname)s] %(message)s'
        self.logger = logging.getLogger(name or __name__)
        self.logger.setLevel(default_logging_level)
        myhandler = logging.StreamHandler()
        myhandler.setFormatter(logging.Formatter(logformat))
        self.logger.addHandler(myhandler)


class Hexo2Hugo(object):
    def __init__(self, src, dest):
        self.src_path = src
        self.dest_path = dest
        self.logger = Logger("hexo2hugo").logger

    def format_head(self):
        if not os.path.exists(self.dest_path):
            os.makedirs(self.dest_path)
        for i in os.listdir(self.src_path):
            file_path = os.path.join(self.src_path, i)
            if os.path.isfile(file_path) and ".md" in i:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.logger.info("{} is formatting".format(i))
                    lines = f.readlines()
                    self._format_tags_categories(lines)
                    self._format_time(lines)
                with open(os.path.join(self.dest_path, i), "w", encoding="utf-8") as nf:
                    self.logger.info("{} is formatted. It writes back".format(i))
                    for j in lines:
                        nf.write(j)
                    self.logger.info("{} is done!".format(i))
                    print()

    def _format_tags_categories(self, lines):
        begin_index = 0
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
        self.logger.info("Tags format result---{}".format(tags))
        self.logger.info("Categories format result---{}".format(categories))

    def _format_time(self, lines):
        time_index = 0
        for i in range(len(lines)):
            if "date:" in lines[i]:
                time_index = i
        time_list = lines[time_index].split(" ")
        result = time_list[0] + " " + time_list[1] + "T" + time_list[2].strip() + "+08:00\n"
        lines[time_index] = result
        self.logger.info("Date format result---{}".format(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', help='Hexo posts directory')
    parser.add_argument('--dest', help='Destination directory')
    parser.add_argument('--debug', help='Output level', action='store_true')
    args = parser.parse_args()

    if args.debug:
        default_logging_level = logging.DEBUG

    hexo2hugo = Hexo2Hugo(args.src, args.dest)
    hexo2hugo.format_head()
