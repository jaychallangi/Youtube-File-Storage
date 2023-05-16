def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        i =0
        while True:
            char1 = file1.read(1)
            char2 = file2.read(1)
            i+=1
            if char1 != char2:
                print(char1)
                print(char2)
                print(i)
                return False
            if not char1:
                return True
        

if compare_files('out_file_name.txt', 'temp.txt'):
    print('The files match')
else:
    print('The files do not match')