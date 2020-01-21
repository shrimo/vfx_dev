# Python data type
import random

# Numeric Types - int, float
var_float = random.uniform(1, 10)
var_int = random.randint(1, 10)
print var_float, type(var_float)
print var_int, type(var_int)

# Sequence Types - str, list, tuple
# var_str = 'abcdef_123'
# print var_str, type(var_str)
# print var_str.split('_')
# str_01 = 'abc'
# str_02 = '123'
# str_03 = str_01.join(str_02)
# str_04 = str_01.upper() + str_02
# print str_03, type(str_03)
# print str_04, type(str_04)

# var_list = range(10)
# print var_list, type(var_list)
# random.shuffle(var_list)
# print var_list
# var_list.sort()
# var_list.append(10)
# print var_list
# print var_list.pop()
# print var_list, len(var_list)

# random.shuffle(var_list)
# print var_list
# for i in range(len(var_list)):
#     print 'index:', i, 'value:', var_list[i]

# for i, v in enumerate(var_list):
#     print 'index:', i, 'value:',v

# var_tulpe = 1, 125, 'tulpe'
# print var_tulpe, type(var_tulpe)

# Set Types
# var_list = [random.randint(1, 5) for i in range(10)]
# var_set = set(var_list)
# print var_list, var_set, type(var_set)

# Mapping Types - dict

var_dict = {'Jon': 0102, 'Rob': 0304, 'Sitve': 0652}
print var_dict, type(var_dict)
var_dict['Arnold'] = 5457
print var_dict, type(var_dict)

for key, val in var_dict.iteritems():
    print key, val

for key in var_dict:
    print key, var_dict[key]

