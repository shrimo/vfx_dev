import os
import nuke

def renamer(old_line, new_line):
    input_file = nuke.root().knob('name').value()
    if not os.path.isfile(input_file):
        print 'no file', input_file
        return
    print 'input file: ', input_file
    print '\n'
    with open(input_file, 'r') as f: 
        data = f.readlines()

    filename, file_extension = os.path.splitext(input_file)
    output_file = filename + '_new' + file_extension
    print 'output file: ', output_file
    f_write = open(output_file, 'w')
    for line in data:
        if old_line in line:
            f_write.write(line.replace(old_line, new_line))
            continue
        f_write.write(line)
    f_write.close()
    print 'rename done'


old_line = 'ld01'
new_line = 'ld02'
renamer(old_line, new_line)
