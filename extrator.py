#!/usr/bin/env python
import csv
import time
from Company import Company
from sys import argv

if __name__ == '__main__':
    if len(argv) < 2:
        config_filename = './config.csv'
    else:
        config_filename = argv[1]

    f = open(config_filename, 'r')
    reader = csv.DictReader(f)
    for company_info in reader:
        print(company_info['company_name'],
                int(company_info['start_index']),
                int(company_info['end_index']))
        start_time = time.time();

        company = Company(
                company_info['url'],
                int(company_info['start_index']),
                int(company_info['end_index']),
                company_info['company_name'],
                int(company_info['max_retry_time']),
                company_info['page_type'], 
                company_info['base_url'])
        last_page_index = company.extract();
        result = company.result;

        result_filename = company_info['company_name'] + '_' \
                + company_info['start_index'] + '_' + \
                str(last_page_index) + '.csv'
        print("Writing collected data into file")
        with open(result_filename, 'w') as fout:
            writer = csv.writer(fout)
            row_to_write = []
            for i in result:
                row_to_write.append(i)
            writer.writerow(row_to_write)

            length = len(result['count'])
            for i in range(length):
                row_to_write = [];
                for j in result:
                    row_to_write.append(result[j][i])
                writer.writerow(row_to_write)

        print("finished, time spent:", time.time() - start_time)

    f.close();


