# B25-based-Information-Retrieval-System

## 1. Large Document Corpus

This file describes the contents of the corpus and associated files, along with their formats.

### 1.1 Documents

The documents are contained in the [documents](documents) directory. Documents are organised in subdirectories according to their document ID. Each file in a subdirectory contains one document. The document ID is the filename. All files are plain text.

### 1.2 Standard Queries

The file ``[queries.txt](files/queries.txt)'' contains the standard queries for evaluation.

Each query is on a new line, with the query ID before the query keywords. In total there are 82 queries.

### 1.3 Relevance Judgments

The file ``[qrels.txt](files/qrels.txt)'' contains the relevance judgments. These are in the [format used by the TREC conference](https://trec.nist.gov/data/qrels_eng/).

Each line has 4 fields, separated by whitespace. The fields are as follows:

 * The Query ID.
 * (this field is always 0 and can be ignored)
 * The Document ID.
 * The relevance judgment. This is 0 for documents that are judged non-relevant. For judged relevant documents, a higher score means a higher level of relevance.

Any document that does not have a relevance judgment for any query is unjudged.

### 1.4 Output Format

A sample output file (with randomly chosen documents) is shown in [sample_output.txt](files/sample_output.txt). This is the format your results should be in.

The format for this is also that used by the TREC conference. This file will have 6 fields on each line, which are:

 * The Query ID.
 * The string "Q0" (this is generally ignored)
 * The Document ID.
 * The rank of the document in the results for this query (starting at 1).
 * The similarity score for the document and this query.
 * The name of the run (this should be your UCD student ID number).

## 2. Small Document Corpus

This file describes the contents of the corpus and associated files, along with their formats.

### 2.1 Documents

The documents are contained in the [documents](documents) directory. Each file in this directory contains one document. The document ID is the filename. All files are plain text.

### 2.2 Standard Queries

The file ``[queries.txt](files/queries.txt)'' contains the standard queries for evaluation.

Each query is on a new line, with the query ID before the query keywords. In total there are 82 queries.

### 2.3 Relevance Judgments

The file ``[qrels.txt](files/qrels.txt)'' contains the relevance judgments. These are in the [format used by the TREC conference](https://trec.nist.gov/data/qrels_eng/).

Each line has 4 fields, separated by whitespace. The fields are as follows:

 * The Query ID.
 * (this field is always 0 and can be ignored)
 * The Document ID.
 * The relevance judgment. For judged relevant documents, a higher score means a higher level of relevance. Any document that does not appear in this file has been judged non-relevant.

In this corpus, there are no unjudged documents.

### 2.4 Output Format

A sample output file (with randomly chosen documents) is shown in [sample_output.txt](files/sample_output.txt). This is the format your results should be in.

The format for this is also that used by the TREC conference. This file will have 6 fields on each line, which are:

 * The Query ID.
 * The string "Q0" (this is generally ignored)
 * The Document ID.
 * The rank of the document in the results for this query (starting at 1).
 * The similarity score for the document and this query.
 * The name of the run (this should be your UCD student ID number).
