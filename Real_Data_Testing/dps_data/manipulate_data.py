import pickle
data1_dict = {}
with open('D:\SURA_QKD\posproc\Real_Data_Testing\dps_data\data1.txt', 'r') as data1:
    for line in data1:
        splittedLine = line.split(';')
        index = int(splittedLine[0])
        val = int(splittedLine[1])
        data1_dict[index] = val
    data1.close()

with open('D:\SURA_QKD\posproc\Real_Data_Testing\dps_data\data1_modified.txt', 'w') as fh:
    for key,val in data1_dict.items():
        fh.write(f'{key}:{val}')
    fh.close()
