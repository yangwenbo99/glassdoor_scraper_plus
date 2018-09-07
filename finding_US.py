#!/usr/bin/python3
import csv
from sys import argv

if __name__ == '__main__':
    if len(argv) < 3:
        print("Usage: ./finding_US.py result.csv US.csv all_1.csv")
        exit()
    result_filename = argv[1]
    us_filename = argv[2]
    all_filenames = argv[3:]
    us_reviews = {}
    fieldnames = []
    with open(us_filename, 'r') as us_file:
        us_reader = csv.DictReader(us_file)
        fieldnames = us_reader.fieldnames
        for i in us_reader:
            us_reviews[i['reviewNo']] = None
    fieldnames.append('from US?')

    with open(result_filename, 'w') as result_file:
        result_writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        result_writer.writeheader()
        for all_filename in all_filenames:
            with open(all_filename, 'r') as all_file:
                all_reader = csv.DictReader(all_file)
                for i in all_reader:
                    if i['reviewNo'] in us_reviews:
                        i['from US?'] = True
                    else:
                        i['from US?'] = False
                    result_writer.writerow(i)




