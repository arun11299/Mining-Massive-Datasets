Mining-Massive-Datasets
=======================

Programs written as part of Coursera's MMDS course by Ullman-Rajaraman-Leskovic.

adwords.py :- Given a set of advertisers, their budget and click through rates, find/choose the advertisers, such
that when the budget of one advertiser finishes choose an advertiser that can bring in maximum revenue based on the
click through rate based upon the impressions (which is limited to 101).

lsh/lsh_test.py: This implements the min hashing technique by shingling of the document lines and creating a signature matrix
for the document lines.
This signature matrix is then fed to the LSH (Location Sensitive hashing) algo code, which finds the best matching lines within
the document. The Jaccard similarity is kept around 0.8 (but the code just displays the best matching lines with a 
difference of 1 word).
