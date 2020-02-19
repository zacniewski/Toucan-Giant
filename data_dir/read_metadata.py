def csv_reader(file_name):
    for row in open(file_name, "r"):
        print(row.strip().split('|'))
        yield row


csv_gen = csv_reader("metadata_m_full.csv")
row_count = 0
for row in csv_gen:
    row_count += 1

print(f"Liczba wierszy to {row_count}")