import math

isDebug = False
class SegmentTree:
    def __init__(self,array) -> None:
        # original array
        self.array_sum = self._fill_to_full(array,0)
        # array of squared value
        self.array_square = [x**2 for x in self.array_sum]
        # segment tree for sum 
        self.tree_sum = self._build_sum_tree(self.array_sum)
        # second st for squared array presentation
        self.square_tree = self._build_sum_tree(self.array_square)
        # so we need two delay-array for controling
        self.delayed_multi = [1]*len(self.tree_sum)
        self.delayed_square = [1]*len(self.tree_sum)
    # make len power of 2 - for simplicity
    def _fill_to_full(self,array,value):
        res = array + [value for _ in range(2**int(math.log(len(array),2)+1)-len(array))]
        return res
    # build tree function, used for both arrays 
    def _build_sum_tree(self,arr):
        n = len(arr)
        tree = [0]*(n-1) + arr
        for i in range(n-2,-1,-1):
            tree[i] = sum(tree[i*2 +1:i*2 + 3])
        return tree
    # main function
    # just rewrite variance formula as sum of (x_i - x_head)^2
    # rewrite this as sum_i_n ( x_i^2 - 2 * x_head + x_head^2)
    # in the end got sum_i (x_i^2) - for this make square_tree
    # sum(x_i) * 2 * x_head and n*x_head()
    # !!! in task descr - answer and formula are differs 
    # I USE FORMULA FOR UNBIASED
    # !!!!! changed to biased as test in server
    def get_variance(self, l, r):
        sum_el_ = self.get_sum(l,r)
        sum_sq_el = self.get_sum_sq(l,r)
        av_el_ = sum_el_ / (r-l)
        return (sum_sq_el + (r-l)*av_el_**2-2*sum_el_*av_el_)/(r-l)
    
    # next sum functions for two segment tree
    def _get_sum(self,block_left, block_right, l, r, node):
        self.check_delayed(node,block_left,block_right)
        if (block_left > block_right or block_left >= r or block_right <= l):
            return 0

        if (block_left >= l and block_right <= r):
            return self.tree_sum[node]
    
        mid = (block_left + block_right) // 2
        return (self._get_sum(block_left, mid, l, r, 2 * node + 1) +
                self._get_sum(mid, block_right, l, r, 2 * node + 2))
    
    def get_sum(self, l, r) :
        n = (len(self.tree_sum) +1)//2
        return self._get_sum(0, n, l, r, 0) 

    def _get_sum_sq(self,block_left, block_right, l, r, node):
        self.check_delayed(node,block_left,block_right)
        
        if (block_left > block_right or block_left >= r or block_right <= l):
            return 0

        if (block_left >= l and block_right <= r):
            return self.square_tree[node]
    
        mid = (block_left + block_right) // 2
        return (self._get_sum_sq(block_left, mid, l, r, 2 * node + 1) +
                self._get_sum_sq(mid, block_right, l, r, 2 * node + 2))
    
    def get_sum_sq(self, l, r) :
        n = (len(self.square_tree) +1)//2
        return self._get_sum_sq(0, n, l, r, 0); 

    # update function  - just add editing of second array - other the same
    def _update(self, i, delta, delta_square,node,block_left, block_right) :
        self.check_delayed(node,block_left,block_right)
        if (i < block_left or i >= block_right) :
            return
        self.square_tree[node] += delta_square
        self.tree_sum[node] += delta
        if (block_right != block_left+1) :
            mid = (block_left+block_right)//2
            self._update(i, delta,delta_square, 2 * node + 1,block_left, mid)
            self._update(i, delta,delta_square, 2 * node + 2,mid, block_right)

    def update(self, i, value):
        n = (len(self.tree_sum) +1)//2
        self._update(i, value - self.get_sum(i,i+1),value**2 - self.get_sum_sq(i,i+1), 0,0, n)


    def print_origin_array(self):
        if isDebug:
            print("+++++++++arrays+++++++++++++")
            print(self.array_sum)
            print(self.array_square)
            print("++++++++++++++++++++++++++++")

    def print_sum_tree(self):
        if isDebug:
            print("+++++++++ trees +++++++++++++")
            print(self.tree_sum)
            print(self.square_tree)
            print("++++++++++++++++++++++++++++")

    # function for checking not submitted changes to st
    def check_delayed(self,node,block_left,block_right):
        if (self.delayed_square[node] != 1):
            self.square_tree[node] *= self.delayed_square[node] 
            if (block_left + 1!= block_right):
                self.delayed_square[node * 2 + 1] *= self.delayed_square[node] 
                self.delayed_square[node * 2 + 2] *= self.delayed_square[node] 
            self.delayed_square[node] = 1
        if (self.delayed_multi[node] != 1):
            self.tree_sum[node] *= self.delayed_multi[node] 
            if (block_left + 1 != block_right):
                self.delayed_multi[node * 2 + 1] *= self.delayed_multi[node] 
                self.delayed_multi[node * 2 + 2] *= self.delayed_multi[node] 
            self.delayed_multi[node] = 1
        
    def _multiply_range(self,node, block_left, block_right, l, r, diff):
        self.check_delayed(node,block_left,block_right)
        if (block_left > block_right or block_left >= r or block_right <= l):
            return 
    
        if (block_left >= l and block_right <= r):
            self.tree_sum[node] *= diff
            self.square_tree[node] *= diff**2
            if (block_left+1!= block_right):
                self.delayed_multi[node * 2 + 1] *= diff
                self.delayed_multi[node * 2 + 2] *= diff
                #square
                self.delayed_square[node * 2 + 1] *= diff**2
                self.delayed_square[node * 2 + 2] *= diff**2
            return
        mid = (block_left + block_right) // 2
        self._multiply_range(node * 2 + 1, block_left, mid, l, r, diff)
        self._multiply_range(node * 2 + 2, mid, block_right, l, r, diff)
        
        self.tree_sum[node] = self.tree_sum[node * 2 + 1] + self.tree_sum[node * 2 + 2]
        self.square_tree[node] = self.square_tree[node * 2 + 1] + self.square_tree[node * 2 + 2]
    
    def multiply_range(self, l, r, multy) :
        n = (len(self.tree_sum) +1)//2
        self._multiply_range(0, 0, n, l, r, multy)

def perform_queries(array, queries):
    res=[]
    tree = SegmentTree(array)
    for query in queries:
        if query[0] == 'get_variance':
            res.append(tree.get_variance(query[1],query[2]))
        elif query[0] == 'update':
            tree.update(query[1],query[2])
        elif query[0] == 'sum_range':
            tree.sum_range(query[1],query[2],query[3])
        elif query[0] == 'multiply_range':
            tree.multiply_range(query[1],query[2],query[3])
            
    return res
