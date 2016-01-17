# Ordoro Code quiz

Instructions to run program:

Create virtualenv and activate it


***virtualenv --python=/path/to/python3 ordoro***

***source ordoro/bin/activate***



Install python modules

***pip install -r requirements.txt***


Run

***python ordoro_test.py***


The complexity of iterate through all users and get emails, april_emails, unique_emails and domain_counts is O(n)
I use a dictionary that keep track of the count of unique domains, then a dict comprehension filter domains with count greater than 1 which is an algorithm with complexity O(m) where m is less or equal than n.


The best case scenario means all emails belong to same domain and complexity such that:

O(n) + O(1) ≈ O(n)

The worst case scenario means all emails domains are different and complexity such that:

O(n) + O(n) = 2(O(n)) ≈ O(n)
