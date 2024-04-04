import json

def new_sample(info_all, file_name, k_time):
    '''try:
        f = open(file_name)
        json.dump(k_time)
        for i in info_all:
            json.dump(i, f)
        json.dump([k_time], f)
        f.close()
    except:
        return False'''
    f = open(file_name, 'w')
    json.dump(['for planets'] + [k_time] + [i for i in info_all], f)
    f.close()
    return True