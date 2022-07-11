#!/usr/bin/python3

"""
program to generate an output file based on an input file which contains certification dates
and gets the certification dates that are within 30 days and keeps them in an output file
"""

import calendar
from bs4 import BeautifulSoup
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="Generates an output file based on the input file that needs all dates "
                                             "less than 30 days to be in the file")
parser.add_argument('-f', '--file', type=str, metavar="input.txt", help="Input file")
args = parser.parse_args()


def main(filename):
    output_list = []
    today = datetime.now()
    input_file = "input_text.txt"
    if filename is not None:
        input_file = filename

    try:
        with open(input_file, 'r') as input_text:
            text = input_text.read()
            scraper = BeautifulSoup(text, 'html.parser')
            # print(, ": now")
            months = list(calendar.month_abbr)
            months.remove('')
            for row in scraper.find_all('tr'):
                line = row.text
                # code to get all the cert lines
                if "Cert" in line:
                    # based on the format of the line it gets the particular date
                    date = line.split('OK:')[1].strip().split(' ')
                    # index of the format
                    # month index = 1
                    # day index = 2
                    # time index = 3
                    # year index = 5

                    cert_time = date[3].split(':')

                    # creates a date time object to compare the date along with the current day

                    day = datetime(int(date[5]), months.index(date[1]) + 1, int(date[2]), int(cert_time[0]),
                                   int(cert_time[1]), int(cert_time[2]))
                    date_difference = day - today
                    output = {
                        "days": "",
                        "line": ""
                    }
                    if date_difference.days > 30:
                        output['days'] = date_difference.days
                        output['line'] = line.strip()
                        output_list.append(output)
    except FileNotFoundError:
        print("================= FATAL ERROR ==================")
        print("Please make sure the name of the file is correct")
        print("================================================")
        exit()

    output_filename = f'output_{str(today).split(".")[0]}.txt'
    try:
        with open(output_filename, 'x') as output_file:
            for line in output_list:
                # amount of days
                output_file.write(f"In {line['days']} days: \n")
                output_file.write(f"{line['line']}\n")
                output_file.write('\n')
    except FileExistsError:
        print("=================================== FATAL ERROR ====================================")
        print("Please wait for a second then try again or remove the previous output file and rerun")
        print("====================================================================================")
        exit()

    print("==================== SUCCESS ===============")
    print(f"File saved as {output_filename}")
    print("============================================")


if __name__ == '__main__':
    main(args.file)
