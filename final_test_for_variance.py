from numpy.core.numeric import isclose
from from_server_test import perform_queries
import numpy as np
import random
import math
import copy
def test_get_variance(size_arr):
    # 20
    random.seed(12)
    array_ = random.sample(range(-size_arr*10, size_arr*10), size_arr)
    left_ = random.randint(0,size_arr-2)
    right_ = random.randint(left_+1,size_arr-1)
    var_  = np.var(array_[left_:right_],ddof=0)
    random.seed(21)
    left_2 = random.randint(0,size_arr-2)
    right_2 = random.randint(left_,size_arr-1)
    var_2  = np.var(array_[left_2:right_2],ddof=0)
    res = perform_queries(array_,[('get_variance',left_,right_),('get_variance',left_2,right_2)])
    print(var_,var_2)
    print(res)
    assert(math.isclose(var_,res[0]) and math.isclose(var_2,res[1]))
    if not math.isclose(var_,res[0]) or not math.isclose(var_2,res[1]):
        print('!!!!!!!!!!!!!!!!')
        print('error in test_get_variance')
        print(res)
        print(var_,var_2)
        print('!!!!!!!!!!!!!!!!')
        return

def test_update(size_arr):
    random.seed(122)
    array_ = random.sample(range(-size_arr*10, size_arr*10), size_arr)
    array_2 = copy.deepcopy(array_)
    random.seed(12)
    list_to_change = random.sample(range(0, size_arr), int(size_arr/10))
    random.seed(2)
    value_for_change = random.sample(range(-size_arr*10, size_arr*10), len(list_to_change))
    for idx_,val_ in zip(list_to_change,value_for_change):
        array_2[idx_] = val_
    req = []
    for idx_,val_ in zip(list_to_change,value_for_change):
        req.append(('update',idx_,val_))
    req.append(('get_variance',0,len(array_)))
    res = perform_queries(array_,req)
    var_  = np.var(array_2,ddof=0)
    print(res)
    print(var_)
    assert(math.isclose(var_,res[0]))
    if not math.isclose(var_,res[0]):
        print('!!!!!!!!!!!!!!!!')
        print('error in test_get_variance')
        print(res)
        print(var_)
        print('!!!!!!!!!!!!!!!!')
        return
def test_from_server():
    array =  [126, 459, -140, 294, 130, 95, 724, 44, 638, -879]
    queries = [('update', 6, 482), ('get_variance', 3, 7), ('update', 4, -231), ('multiply_range', 1, 5, -1), ('get_variance', 5, 9), ('get_variance', 0, 8), ('update', 9, 499), ('update', 2, 267), ('get_variance', 2, 4), ('update', 4, -160)]
    res = perform_queries(array,queries)
    assert(res == [23546.1875, 63514.6875, 76573.234375, 78680.25])
    if res != [23546.1875, 63514.6875, 76573.234375, 78680.25]:
        print('!!!!!!!!!!!!!!!!')
        print('error in test_from_server')
        print('!!!!!!!!!!!!!!!!')
        return
def _update_query(array_copy,queries):
    idx_ = random.randint(0,len(array_copy) -1)
    new_val = random.randint(-len(array_copy)*10,len(array_copy)*10)
    array_copy[idx_] = new_val
    queries.append(('update', idx_, new_val))
def _get_var_query(array_copy,queries,check_arr):
    left_ = random.randint(0,len(array_copy)-2)
    right_ = random.randint(left_+1,len(array_copy)-1)
    var_  = np.var(array_copy[left_:right_],ddof=0)
    check_arr.append(var_)
    queries.append(('get_variance', left_, right_))
def _get_multiply_query(array_copy,queries):
    multyplier_ = random.randint(-1000,10000)
    left_ = random.randint(0,len(array_copy)-2)
    right_ = random.randint(left_+1,len(array_copy)-1)
    for i in range(left_,right_):
        array_copy[i] *= multyplier_
    queries.append(('multiply_range', left_, right_, multyplier_))
def random_test_based_on_server(size_arr):
    array_ = random.sample(range(-size_arr*10, size_arr*10), size_arr)
    array_copy = copy.deepcopy(array_)
    queries = []
    check_arr = []
    #('update', 6, 482), 
    _update_query(array_copy,queries)
    # ('get_variance', 3, 7), 
    _get_var_query(array_copy,queries,check_arr)
    # ('update', 4, -231),
    _update_query(array_copy,queries)
    # ('multiply_range', 1, 5, -1),
    _get_multiply_query(array_copy,queries)
    #  ('get_variance', 5, 9), 
    _get_var_query(array_copy,queries,check_arr)
    # ('get_variance', 0, 8),
    _get_var_query(array_copy,queries,check_arr)
    #  ('update', 9, 499), 
    _update_query(array_copy,queries)
    # ('update', 2, 267),
    _update_query(array_copy,queries)
    # ('get_variance', 2, 4),
    _get_var_query(array_copy,queries,check_arr)
    # ('update', 4, -160)
    _update_query(array_copy,queries)
    # full variance
    var_  = np.var(array_copy,ddof=0)
    check_arr.append(var_)
    queries.append(('get_variance', 0, len(array_copy)))
    res = perform_queries(array_,queries)
    for x,y in zip(check_arr,res):
        print(x,y)
        assert(np.isclose(x,y))
    print(np.var(array_,ddof=0))
def random_seq_of_query(size_seq,size_arr):
    seq_ = random.sample(range(0, size_seq*10), size_seq)
    seq_ = [x % 3 for x in seq_]
    array_ = random.sample(range(-size_arr*10, size_arr*10), size_arr)
    array_copy = copy.deepcopy(array_)
    queries = []
    check_arr = []
    for comm in seq_:
        if comm == 0:
            _update_query(array_copy,queries)
        elif comm == 1:
            _get_var_query(array_copy,queries,check_arr)
        elif comm == 2:
            _get_multiply_query(array_copy,queries)
    var_  = np.var(array_copy,ddof=0)
    check_arr.append(var_)
    queries.append(('get_variance', 0, len(array_copy)))
    print(queries)
    res = perform_queries(array_,queries)
    for x,y in zip(check_arr,res):
        print(x,y)
        assert(np.isclose(x,y))
    print(np.var(array_,ddof=0))
def test_multiply_range(size_arr):
    random.seed(12)
    array_ = random.sample(range(-size_arr*10, size_arr*10), size_arr)
    array_copy = copy.deepcopy(array_)
    multyplier_ = random.randint(-1000,10000)
    random.seed(32)
    multyplier_2 = random.randint(-1000,10000)
    left_ = random.randint(0,size_arr-2)
    right_ = random.randint(left_+1,size_arr-1)
    left_2 = random.randint(0,size_arr-2)
    right_2 = random.randint(left_,size_arr-1)
    for i in range(left_,right_):
        array_copy[i] *= multyplier_
    for i in range(left_2,right_2):
        array_copy[i] *= multyplier_2
    var_ = np.var(array_,ddof=0)
    var_2 = np.var(array_copy,ddof=0)
    res = perform_queries(array_,[('get_variance',0,len(array_)),\
                                    ('multiply_range', left_, right_, multyplier_),\
                                    ('multiply_range', left_2, right_2, multyplier_2),\
                                    ('get_variance',0,len(array_))])
    print(var_,var_2)
    print(res)
    assert(math.isclose(var_,res[0]) and math.isclose(var_2,res[1]))
    if not math.isclose(var_,res[0]) or not math.isclose(var_2,res[1]):
        print('!!!!!!!!!!!!!!!!')
        print('error in test_multiply_range')
        print(res)
        print(var_,var_2)
        print('!!!!!!!!!!!!!!!!')
        return
def init_test_from_task():
    array = [10, 2, 3, 4, 5]
    queries = [('get_variance', 0, 2), ('multiply_range', 3, 5, 10), ('update', 3, 10), ('get_variance', 2, 5)]
    res = perform_queries(array,queries)
    assert(res == [16.0, 428.6666666666667])
    if res != [16.0, 428.6666666666667]:
        print('!!!!!!!!!!!!!!!!')
        print('error in init_test_from_task')
        print('!!!!!!!!!!!!!!!!')
        return
def some_random_test():
    for i in range(50):
        random.seed(i)
        array_ = random.sample(range(10, 300), 20)
        array_2 = copy.deepcopy(array_)
        array_2[3] *= 10 
        array_2[4] *= 10
        array_2[3] = 10
        #print(array_)
        var_  = np.var(array_[:2],ddof=0)
        var_2  = np.var(array_2[2:5],ddof=0)
        res = perform_queries(array_,[('get_variance', 0, 2), ('multiply_range', 3, 5, 10), ('update', 3, 10), ('get_variance', 2, 5)])
        print(res)
        print(var_,var_2)
        assert(math.isclose(var_,res[0]) and math.isclose(var_2,res[1]))
        if not math.isclose(var_,res[0]) or not math.isclose(var_2,res[1]):
            print(res)
            print(var_,var_2)
            print('break')
            break
def main():
    test_get_variance(20)
    test_get_variance(200)
    test_get_variance(1000)
    test_get_variance(10000)
    test_update(20)
    test_update(200)
    test_update(1000)
    test_update(10000)
    test_from_server()
    some_random_test()
    init_test_from_task()
    test_multiply_range(20)
    test_multiply_range(200)
    test_multiply_range(1000)
    test_multiply_range(10000)
    random_test_based_on_server(20)
    random_test_based_on_server(200)
    random_test_based_on_server(2000)
    random_test_based_on_server(20000)
    random_seq_of_query(10,50)
    random_seq_of_query(100,1000)
    random_seq_of_query(200,2000)
main()

