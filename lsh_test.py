import sys
import time
import numpy as np
import operator

union_shingles = set()
union_shingles_dict = dict()
doc_lists = []
hash_list = []
minh_mat = []

num_hashes = 240        ## better to keep this as multiple of rows_per_band
rows_per_band = 24 

words_per_line = dict()

INT_MAX = sys.maxint

def read_file():
    global union_shingles, doc_lists
    index = 0

    with open("processed_file.txt", 'r') as f:
        for line in f:
            shingle = line.rstrip().split(" ")
#k_shingle = [i+j for i,j in zip(shingle[::3], shingle[1::3])]
            union_shingles.update(shingle)
            doc_lists.append(shingle)
            words_per_line[index] = len(shingle)
            index = index + 1

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
    global hash_list, union_shingles, num_hashes
    for shingle in union_shingles:
        hash_list.append(generate_hash(shingle, num_hashes))

def convert_set_2_list():
    global union_shingles
    union_shingles = list(union_shingles)

# Create a sparse matrix representation scheme
def prep_sparse_matrix():
    global union_shingles, doc_lists

    for i, doc_list in enumerate(doc_lists):
        idxs = []
        for word in doc_list:
            try:
                idx = union_shingles.index(word)
            except ValueError, e:
                idx = 0 

            if idx != 0:
                idxs.append(idx)
            
        doc_lists[i] = idxs
        doc_lists[i].sort()

def create_minhash_matrix():
    global minh_mat, doc_lists, hash_list

    for idx, hashes in enumerate(hash_list):
        tmp_docs = []
        for doc_no, doc_list in enumerate(doc_lists):
            if idx in doc_list:
                tmp_docs.append(doc_no)
           
        for h_idx, hash in enumerate(hashes):
            for tmp_doc in tmp_docs:
                if minh_mat[h_idx][tmp_doc] == -1 or \
                   minh_mat[h_idx][tmp_doc] > hash:
                    minh_mat[h_idx][tmp_doc] = hash

    return

if __name__ == "__main__":
    start_time = time.time()

    read_file()
    print "read file done"

    populate_hash_list()
    print "populate hash list done"

    convert_set_2_list()
    print "converting set to list done"

    prep_sparse_matrix()
    print "Preparation of sparse matrix done"

    minh_mat = np.empty((num_hashes, len(doc_lists,)))
    minh_mat[:] = -1

    create_minhash_matrix()
    print "Creation of minhash matrix done"

    print minh_mat

## Apply LSH, divide the signature matrix
## into bands and hash them
## for 12 hash, divide into 3 bands having 4
## rows each.
    """
    doc_hashs = dict()
    
    for doc in xrange(len(doc_lists)):
        doc_hashs[doc] = 0
        for i in xrange(rows_per_band):
            doc_hashs[doc] = doc_hashs[doc] +  i * minh_mat[i][doc] 
    """

    ## second method (This is not true LSH)
    ## Dont have to compare like insertion sort
    ## Comparison moves fwd, if a = b, its not stupid
    ## to assume that b = a
    matches = dict()
    start = 0
    offset = rows_per_band
    steps = (num_hashes / rows_per_band)
##steps = 1  ## Just for testing
    blacklist = dict()

    h_start = 0

    while steps > 0:
        while start != len(doc_lists) - 1:
            matches[start] = []
            blacklist[start] = dict()
            curr_wpl = words_per_line[start]

            for col in xrange(start + 1, len(doc_lists)):
                mismatches = 0
                err = False
                ## If there are more words then there is no 
                ## point in comparing
                if abs(curr_wpl - words_per_line[col]) > 1:
                    continue

                if blacklist[start].has_key(col):
                    continue

                for h_row in xrange(h_start, h_start + offset):
                    if minh_mat[h_row][start] != minh_mat[h_row][col]:
                        mismatches = mismatches + 1

                    if mismatches > 1:      ## Edit distance must not be more than one
                        blacklist[start][col] = True
                        err = True
                        break

                if not err:
                    matches[start].append(col)
            start = start + 1

        steps = steps - 1
        h_start = h_start + rows_per_band

    print matches
    for match in matches:
        if len(matches[match]) > 0:
            print "{0} => {1}\n".format(match, str(matches[match]))


    # Find the best matching pairs with jaccard similarity >= 0.8

    
##print "Preparation of doc hash done"

    ## Sort doc_hashes by value for the time being
##sorted_x = sorted(doc_hashs.items(), key=operator.itemgetter(1))
##print sorted_x
    elapsed_time = time.time() - start_time
    print "Elapsed time is %s" % str(elapsed_time)
