# תאריך
# שם לקוח
# שם תיק
# פירוט
# עובד (גלית)
# שעות
# הוצאות - 

# Tasks:
# X All the data to the input file
# X Add worker name as "גלית"
# X Add a summery of how many hours of work each day
# X Show the days that didn't have enought work (that are not weekends)
# 5. Fix incorrect lines

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

import re
import csv
from datetime import datetime

dic = {}

def parse_line(line):
    # Using regex to extract data from each line
    pattern = r'^(.*?)\s*-\s*(.*?)\s*-\s*(.*?)(?: - הוצאות)?\s*-\s*([\d\.]*?)\s*;'
    match = re.match(pattern, line)
    if match:
        clientName, workCase, details, hours = match.groups()
        # spending, hours = (hours, 0) if 'הוצאות' in line else ('', hours)
        worker = 'הוצאות' if 'הוצאות' in line else 'גלית'
        return [clientName, workCase, details, worker, hours]
    else:
        print("no match found for ", line[::-1])
        return None

def main():
    input_file = "input.txt"
    output_file = "output.csv"

    data_blocks = []
    current_date = None
    current_data = []
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        lines = [line.strip() for line in lines]

        for line in lines:
            # Check if the line is a date line
            if re.match(r'^\d+\.\d+\.\d+', line):
                # Save the previous text block (if any)
                if current_date and current_data:
                    data_blocks.append((current_date, current_data))
                    current_data = []

                # Update the current date
                current_date = line.strip()
            else:
                # Parse the data lines for this text block
                data = parse_line(line)
                if data and 'הוצאות' not in data:
                    if data is not None and is_float(data[4]):
                        dic[current_date] = dic.get(current_date, 0) + float(data[4])
                    else:
                        print(f"error in line {line} with {data[4]}")
                if data:
                    current_data.append(data)

        # Save the last text block (if any)
        if current_date and current_data:
            data_blocks.append((current_date, current_data))

    # Sort data blocks based on the date
    data_blocks.sort(key=lambda x: datetime.strptime(x[0], '%d.%m.%Y'))

    # Write the combined data to the output CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)

        # Write the header row
        writer.writerow(["תאריך", "שם לקוח", "שם תיק", "פירוט", "עובד", "שעות", "הוצאות"])

        for date, data_rows in data_blocks:
            # Write the data rows to the CSV
            for data in data_rows:
                # data.insert(3, "גלית")
                writer.writerow([date] + data)

    # Print the dates that are included in the output CSV file
    # included_dates = sorted(set([datetime.strptime(date, '%d.%m.%Y') for date, _ in data_blocks]))
    # print("Dates included in the output CSV file:")
    # print("\n".join([date_obj.strftime('%d.%m.%Y') for date_obj in included_dates]))
    
    # sort the dict
    sorted_items = sorted(dic.items(), key=lambda item: datetime.strptime(item[0], '%d.%m.%Y'))
    print("\n".join([f"{item[0]} {str(item[1])}{' <-- NOTE' if item[1] < 7 else ''}" for item in sorted_items]))

if __name__ == "__main__":
    main()
