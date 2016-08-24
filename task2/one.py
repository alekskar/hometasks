list_keys = ['key1', 'key2', 'key3', 'key4']
list_values = [1, 2, 3]


def function(keys, values):
    dict1 = {}
    for i in range(len(keys)):
        if i < len(values):
            dict1[keys[i]] = values[i]
        else:
            dict1[keys[i]] = 'None'
    return dict1
a = function(list_keys, list_values)
print(a)
for i in a:
    print(i, a[i])




