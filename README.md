# BM25-based Information Retrieval (IR) System

## 1. System-v1 - Dealing with Large Document Corpus

This file describes the contents of the corpus and associated files, along with their formats.

```
.
|-- documents
|-- files
|   |-- __pycache__
|   |   `-- porter.cpython-39.pyc
|   |-- output.txt
|   |-- porter.py
|   |-- qrels.txt
|   |-- queries.txt
|   |-- sample_output.txt
|   |-- simple_output.txt
|   |-- stopwords.txt
|   `-- terms_large.txt
`-- search_large.py
```

### 1.1 Documents

The documents are contained in the "documents" directory. Documents are organised in subdirectories according to their document ID. Each file in a subdirectory contains one document. The document ID is the filename. All files are plain text.

### 1.2 Standard Queries

The file "files/queries.txt'' contains the standard queries for evaluation.

Each query is on a new line, with the query ID before the query keywords. In total there are 82 queries.

### 1.3 Relevance Judgments

The file "files/qrels.txt'' contains the relevance judgments. These are in the [format used by the TREC conference](https://trec.nist.gov/data/qrels_eng/).

Each line has 4 fields, separated by whitespace. The fields are as follows:

 * The Query ID.
 * (this field is always 0 and can be ignored)
 * The Document ID.
 * The relevance judgment. This is 0 for documents that are judged non-relevant. For judged relevant documents, a higher score means a higher level of relevance.

Any document that does not have a relevance judgment for any query is unjudged.

### 1.4 Output Format

A sample output file (with randomly chosen documents) is shown in "files/sample_output.txt". This is the format your results should be in.

The format for this is also that used by the TREC conference. This file will have 6 fields on each line, which are:

 * The Query ID.
 * The string "Q0" (this is generally ignored)
 * The Document ID.
 * The rank of the document in the results for this query (starting at 1).
 * The similarity score for the document and this query.
 * The name of the run (this should be your UCD student ID number).

### 1.5 A Sample Output for Query Manually
```
---------------------Read/Generate/Write File time: 2.3000000000002185e-05 sec.-------------
Wait for a moment, please, building index of BM25 from file ...
---------------------Build Index of B25 time: 4.488414 sec.---------------------------------
Enter query: hello

Result for query [hello]
1 GX016-68-8167726 5.040544
2 GX022-73-15765418 4.840700
3 GX027-42-8507420 4.166417
4 GX181-61-5790115 2.948497
5 GX000-49-12224349 2.634025
6 GX000-63-3636455 2.508728
7 GX001-22-5770689 2.490494
8 GX002-59-5385286 2.374683
9 GX001-84-3895877 2.294411
10 GX002-55-1145531 2.061862
11 GX011-91-3185599 1.544885
12 GX031-32-8523562 1.540457
13 GX014-67-16759661 1.513768
14 GX017-03-1777733 1.428711
15 GX048-21-3302291 1.175930
---------------------Execute Query Time: 0.0014739999999999753 sec.-------------------------
```

### 1.6 Evaluation Output
```
Wait for a moment, please, reading document from documents folder ...
---------------------Read/Generate/Write File Time: 35.267461 sec.--------------------------
Wait for a moment, please, building index of BM25 from file ...
---------------------Build Index of B25 Index Time: 4.8913749999999965 sec.-----------------
Evaluation results:
Precision: 0.3501
Recall: 0.9110
P@10: 0.5074
R-precision: 0.4959
MAP: 0.5136
bpref: 0.5153
NDCG: 0.4941
---------------------System Overall Run Time: 40.348432 sec.--------------------------------
```

## 2. System-v2 - Dealing with Small Document Corpus

This file describes the contents of the corpus and associated files, along with their formats.

```
.
|-- documents
|-- files
|   |-- __pycache__
|   |   `-- porter.cpython-39.pyc
|   |-- output.txt
|   |-- porter.py
|   |-- qrels.txt
|   |-- queries.txt
|   |-- sample_output.txt
|   `-- stopwords.txt
`-- search_small.py
```

### 2.1 Documents

The documents are contained in the "documents" directory. Each file in this directory contains one document. The document ID is the filename. All files are plain text.

### 2.2 Standard Queries

The file "files/queries.txt'' contains the standard queries for evaluation.

Each query is on a new line, with the query ID before the query keywords. In total there are 82 queries.

### 2.3 Relevance Judgments

The file "files/qrels.txt'' contains the relevance judgments. These are in the [format used by the TREC conference](https://trec.nist.gov/data/qrels_eng/).

Each line has 4 fields, separated by whitespace. The fields are as follows:

 * The Query ID.
 * (this field is always 0 and can be ignored)
 * The Document ID.
 * The relevance judgment. For judged relevant documents, a higher score means a higher level of relevance. Any document that does not appear in this file has been judged non-relevant.

In this corpus, there are no unjudged documents.

### 2.4 Output Format

A sample output file (with randomly chosen documents) is shown in "files/sample_output.txt". This is the format your results should be in.

The format for this is also that used by the TREC conference. This file will have 6 fields on each line, which are:

 * The Query ID.
 * The string "Q0" (this is generally ignored)
 * The Document ID.
 * The rank of the document in the results for this query (starting at 1).
 * The similarity score for the document and this query.
 * The name of the run (this should be your UCD student ID number).

### 2.5 A Sample Output for Query Manually
```
Enter query: we

Result for query [we]
1 472 9.525564
2 914 9.277455
3 775 9.030070
4 1110 8.188895
5 607 8.034218
6 1380 7.814416
7 1148 7.478861
8 817 7.361434
9 138 7.296771
10 934 7.259112
11 730 7.148433
12 228 7.065598
13 355 6.995317
14 587 6.792621
15 489 6.305406
---------------------Execute Query Time: 0.000795000000000004 sec.--------------------------
```

### 2.6 Evaluation Output
```
---------------------Read/Generate/Write File Time: 3.0000000000002247e-05 sec.-------------
Wait for a moment, please, building index of BM25 from file ...
---------------------Build Index of B25 Index Time: 0.049407 sec.---------------------------
Evaluation results:
Precision: 0.0982
Recall: 0.6543
P@10: 0.2911
R-precision: 0.3803
MAP: 0.3928
bpref: 0.3623
NDCG: 0.3808
---------------------System Overall Run Time: 0.156583 sec.---------------------------------
```
