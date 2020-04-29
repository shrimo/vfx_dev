import sys
import os

def renamer(input_file_name, output_file_name, old_line, new_line):
    if not os.path.isfile(input_file_name):
        print 'no file', input_file_name
        return
    print 'input file: ', input_file_name
    print 'output file: ', output_file_name
    print '\n'
    with open(input_file_name, 'r') as f: 
        data = f.readlines()
    f_write = open(output_file_name, 'w')
    for line in data:
        if old_line in line:
            f_write.write(line.replace(old_line, new_line))
            continue
        f_write.write(line)
    f_write.close()
    print 'rename done'


if __name__ == "__main__":
    old_line = 'ld01'
    new_line = 'ld02'
    renamer(sys.argv[1], sys.argv[2], old_line, new_line)
