import csv
import re

###     This code is checking big one column (Img_url or Detail_URL) of small_file from big_file,
###     if it is not available the output file will have empty row
###     and if matches then output file will have the data of small_file

big_file = 'Filtter Data/Crowe - Dutch with Detail URl.csv'  # Replace with your first CSV file path
small_file = 'Filtter Data/Crowe - Record.csv'  # Replace with your first CSV file path
def read_csv_to_dict_list(csv_file):
    data_list = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_list.append(dict(row))
    return data_list

big_list = read_csv_to_dict_list(big_file)
small_list = read_csv_to_dict_list(small_file)

def remove_bom_from_keys(data):
    return {key.lstrip('\ufeff'): value for key, value in data.items()}


output_file = 'Output/Crowe - Updated.csv'

count = 0
for big in big_list:
    found_img = False
    count += 1
    # big_file_img = big.get('Img_url')
    big_file_img = big.get('Detail_URL').replace('nl-nl/','')

    if big_file_img:
        for small_file in small_list:
            # small_file_img = small_file.get('Img_url')
            small_file_img = small_file.get('Detail_URL').replace('nl-nl/','')

            if small_file_img:
                # small_file_img_code = re.search(r'ch-asset-(\d+)', small_file_img)
                # small_file_img_code = small_file_img_code.group(1) if small_file_img_code else None
                # big_file_img_code = re.search(r'ch-asset-(\d+)', big_file_img)
                # big_file_img_code = big_file_img_code.group(1) if big_file_img_code else None
                small_file_img_code = re.search(r'spark/(.*)', small_file_img).group(1)
                big_file_img_code = re.search(r'spark/(.*)', big_file_img).group(1)


                if small_file_img_code == big_file_img_code:
                    print(count, " Got that, Now save the data : ", small_file)
                    found_img = True

                    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['Title', 'Date', 'Content', 'Img_url', 'Detail_URL']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        if csvfile.tell() == 0:
                            writer.writeheader()
                        small_file_cleaned = remove_bom_from_keys(small_file)
                        writer.writerow(small_file_cleaned)
                        print(count, 'Data Saved successfully')
                    break

        if found_img == False:
            print(count,' Empty')
            with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Title', 'Date', 'Content', 'Img_url', 'Detail_URL']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if csvfile.tell() == 0:
                    writer.writeheader()
                # writer.writerow({field: '' for field in fieldnames})
                small_file_cleaned = dict()
                small_file_cleaned['Detail_URL'] = big.get('Detail_URL')
                writer.writerow(small_file_cleaned)
                print(count, 'Data Saved successfully')

    else:
        print(count,'Empty')
        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Date', 'Content', 'Img_url', 'Detail_URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            # writer.writerow({field: '' for field in fieldnames})
            small_file_cleaned = dict()
            small_file_cleaned['Detail_URL'] = big.get('Detail_URL')
            writer.writerow(small_file_cleaned)
            print(count, 'Data Saved successfully')



'''         
########### 2 files with same columns and sorting 2nd file in order of 1st file by comparing column "Title".

import csv

# Read the first file and get the order of titles
with open('Input/bimfmf_data - Unsorted CSV.csv', 'r', encoding='utf-8') as f1:
    reader1 = csv.DictReader(f1)
    title_order = [row['Title'] for row in reader1]

# Read the second file into a list of dictionaries
with open('Input/Crowe - Dutch with Detail URl.csv', 'r', encoding='utf-8') as f2:
    reader2 = csv.DictReader(f2)
    data = list(reader2)

# Sort the data from the second file based on the title order in the first file
sorted_data = sorted(data, key=lambda x: title_order.index(x['Title']))

# Write the sorted data back to the second file
with open('file2_sorted.csv', 'w', newline='', encoding='utf-8') as f_out:
    writer = csv.DictWriter(f_out, fieldnames=reader2.fieldnames)
    writer.writeheader()
    writer.writerows(sorted_data)

print("File sorted and saved as file2_sorted.csv")


'''