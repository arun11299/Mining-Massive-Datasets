import sys
import time
import numpy as np
import operator

union_shingles = set()
union_shingles_dict = dict()
doc_lists = []
hash_list = []
minh_mat = []

INT_MAX = sys.maxint

def read_file():
    global union_shingles, doc_lists

    with open("pre_proc_file.txt", 'r') as f:
        for line in f:
            shingle = line.rstrip().split(" ")
            k_shingle = [i+j for i,j in zip(shingle[::3], shingle[1::3])]
            union_shingles.update(k_shingle)
            doc_lists.append(k_shingle)

def print_shingles():
    global union_shingles 
    print union_shingles

def print_doc_lists():
    global doc_lists
    print doc_lists

def print_hash_list():
    global hash_list
    print hash_list

def generate_hash(shingle, count):
    global union_shingles

    l = []
    p = len(union_shingles)
    for i in xrange(count):
        l.append((hash(shingle) + i * hash(shingle[::-1])) % p)

    return l

def populate_hash_list():
    global hash_list, union_shingles
    for shingle in union_shingles:
        hash_list.append(generate_hash(shingle, 200))

def convert_set_2_list():
    global union_shingles
    union_shingles = list(union_shingles)

def convert_set_2_dict():
    global union_shingles, union_shingles_dict
    for i, j in enumerate(union_shingles):
        union_shingles_dict[j] = i


# Create a sparse matrix representation scheme
def prep_sparse_matrix():
    global union_shingles_dict, doc_lists
    print len(doc_lists)
    for i, doc_list in enumerate(doc_lists):
        idxs = []
	if i % 2000 == 0:
	    print "Batch done"
	
	d = dict()

        for word in doc_list:
            try:
                idx = union_shingles_dict[word]
                d[idx] = True
            except KeyError, e:
                idx = 0 
            """
            if idx != 0:
                idxs.append(idx)
            """
            
        doc_lists[i] = d
##doc_lists[i].sort()

def create_minhash_matrix():
    global minh_mat, doc_lists, hash_list

    for idx, hashes in enumerate(hash_list):
        tmp_docs = []
        for doc_no, doc_list in enumerate(doc_lists):
            if doc_list.has_key(idx):
                tmp_docs.append(doc_no)
           
        for h_idx, hash in enumerate(hashes):
            for tmp_doc in tmp_docs:
                if minh_mat[h_idx][tmp_doc] == -1 or \
                   minh_mat[h_idx][tmp_doc] > hash:
                    minh_mat[h_idx][tmp_doc] = hash
    print minh_mat

    return

if __name__ == "__main__":
    start_time = time.time()

    read_file()
    print "read file done"

    populate_hash_list()
    print "populate hash list done"

    convert_set_2_dict()
    print "converting set to list done"

    prep_sparse_matrix()
    print "Preparation of sparse matrix done"

    minh_mat = np.empty((200, len(doc_lists,)))
    minh_mat[:] = -1

    create_minhash_matrix()
    print "Creation of minhash matrix done"
#print minh_mat

## Apply LSH, divide the signature matrix
## into bands and hash them
## for 12 hash, divide into 3 bands having 4
## rows each.
    doc_hashs = dict()
    
    for doc in xrange(len(doc_lists)):
        doc_hashs[doc] = 0
        for i in xrange(20):
            doc_hashs[doc] = doc_hashs[doc] + i * minh_mat[i][doc] 
    print "Preparation of doc hash done"

    ## Sort doc_hashes by value for the time being
    sorted_x = sorted(doc_hashs.items(), key=operator.itemgetter(1))
    print sorted_x
    elapsed_time = time.time() - start_time
    print "Elapsed time is %s" % str(elapsed_time)
