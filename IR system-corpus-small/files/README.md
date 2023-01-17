### Xibo Wang IR Assignment

##### What my program can do

My program can work on both small and large corpus. Because the relevance judge for small and large qrels.txt is not the same. I need to write two separate files:  **search_small.py** and **search_large.py** to operate on different corpus.

When test small corpus, print '**python search_small.py -m manual**' to enter query manually or print '**python search_small.py -m evaluation**' to run the evaluation in Terminal.

When test large corpus, print '**python search_large.py -m manual**' to enter query manually or print '**python search_large.py -m evaluation**' to run the evaluation in Terminal.

