import math
import re
import time
import argparse
import os
import string
from files import porter

# Store stemming words in a global variable avoids stemming many times, which can greatly improve efficiency.
stem_dict = dict()


# Read stopwords.txt file and store stopwords in set data structure.
def get_stopwords() -> set:
    stopword_set = set()
    with open('./files/stopwords.txt', 'r') as lines:
        for line in lines:
            stopword_set.add(line.rstrip())
    return stopword_set


# The function is to read all documents from "files" then put them into a dictionary.
# Four tips about dealing with content in each document.
# * Strip punctuation in all documents
# * Convert all content to lower case in all documents.
# * Get tokens using split(" ").
# * Once tokens is extracted term, strip stopwords and stem each token.
def read_documents():
    print("Wait for a moment, please, reading document from documents folder ...")
    stopwords_set = get_stopwords()
    stemmer = porter.PorterStemmer()
    files = os.listdir('./documents')
    terms_dict = dict()
    N = 0
    sum_length = 0
    document_length = dict()
    for file in files:
        N += 1
        position = './documents/' + file
        document_len = 0
        with open(position, 'r') as each_file:
            content = each_file.read()
            content = re.sub(r'[{}]+'.format(string.punctuation), '', content)
            content = content.lower()
            words = content.split()
            for term in words:
                if term not in stopwords_set:
                    if term not in stem_dict:
                        stem_dict[term] = stemmer.stem(term)
                    term = stem_dict[term]
                    document_len += 1
                    if term not in terms_dict:
                        terms_dict[term] = [(file, 1)]
                    else:
                        document_id, frequency = terms_dict[term][-1]
                        if document_id == file:
                            frequency += 1
                            terms_dict[term][-1] = (document_id, frequency)
                        else:
                            terms_dict[term].append((file, 1))
        document_length[file] = document_len
        sum_length += document_len
    for term in terms_dict:
        n_i = len(terms_dict[term])
        terms_dict[term].insert(0, n_i)
    average_length = sum_length / N
    return terms_dict, average_length, N, document_length


# This function is to find retrieved documents for each query in the output.txt file.
def find_retrieved_documents() -> dict:
    retrieved_dict = dict()
    with open('files/outputt.txt', 'r') as lines:
        for line in lines:
            line = line.replace('\n', '')
            words_list = line.split(' ')
            query_id = words_list[0]
            doc_word = words_list[2]
            rank = int(words_list[3])
            if query_id not in retrieved_dict:
                retrieved_dict[query_id] = list()
                retrieved_list = retrieved_dict[query_id]
                retrieved_list.append([doc_word, rank])
            else:
                retrieved_list = retrieved_dict[query_id]
                retrieved_list.append([doc_word, rank])
    return retrieved_dict


# In order to improve the efficiency of judging documents.
# this function only stores relevant documents in the dictionary.
# In this way, the system does not need to judge the relevant points again in the evaluation.
def find_relevant_documents() -> dict:
    relevant_dict = dict()
    with open('./files/qrels.txt', 'r') as lines:
        for line in lines:
            line = line.replace('\n', '')
            line = line.strip()
            words_list = line.split(' ')
            query_id = words_list[0]
            document_word = words_list[2]
            relevant_degree = int(words_list[-1])
            if query_id in relevant_dict:
                document_dict = relevant_dict[query_id]
                if relevant_degree != 0 and document_word not in document_dict:
                    document_dict[document_word] = relevant_degree
            else:
                relevant_dict[query_id] = dict()
                document_dict = relevant_dict[query_id]
                if relevant_degree != 0 and document_word not in document_dict:
                    document_dict[document_word] = relevant_degree
    return relevant_dict


# The function is to build the system's index.
# Stored Format: each term separated by '   /' and stores every document which contains this term BM25 score.
# split(   /\n) function is to split terms and scores.
# I use a dictionary data structure to store index. Key in dict is unique terms. Value is a list including document ID and term score in this document.

# My Design Idea to enhance efficiency is: Split terms and search for index and put all scores in the list for each query.
# As I need to iterate all documents which contain the term, the list will not bring complexity in the following process.

# The build index algorithm is efficient and skillful because it does not need to do extra calculation such as not needing to do another judgement again.
# as all documents that I need are already stored in the list.
def build_term_index() -> dict:
    print("Wait for a moment, please, building index of BM25 from file ...")
    term_index = dict()
    file = open('./files/terms_small.txt', 'r')
    document_items = file.read().split('   /\n')
    file.close()
    for item in document_items:
        document_list = list()
        item = item.split()
        # term is the first element of item list
        # So we can use loop to get ID of document and each term's score in corresponding document
        if item != '/':
            count = 1
            term = item[0]
            while count < len(item) - 1:
                document_id = item[count]
                score = item[count + 1]
                count += 2
                document_list.append((document_id, float(score)))
            term_index[term] = document_list
    return term_index


# The function is to execute the query operation and calculate the score of the query into the result set.
# My system utilizes a dictionary to store each document's similarity with the query.
# And add BM25 score for each term as the value of the dictionary.
# To enhance efficiency, in order to avoid calculated scores of terms repeatedly. For each query, I stored the unique token in the set.
def execute_query(term_index: dict):
    stemmer = porter.PorterStemmer()
    stopwords_set = get_stopwords()
    entered_query = input('Enter query: ')
    while entered_query != 'QUIT':
        query_start_time = time.process_time()
        documents = dict()
        entered_query = entered_query.lower()
        entered_query = re.sub(r'[{}]+'.format(string.punctuation), '', entered_query)
        tokens = entered_query.split()
        unique_tokens_set = set()
        for term_query in tokens:
            if term_query not in stopwords_set:
                if term_query not in stem_dict:
                    stem_dict[term_query] = stemmer.stem(term_query)
                term_query = stem_dict[term_query]
                if term_query not in unique_tokens_set:
                    unique_tokens_set.add(term_query)
                else:
                    continue
                if term_query in term_index:
                    for document_id, score in term_index[term_query]:
                        if document_id not in documents:
                            documents[document_id] = score
                        else:
                            documents[document_id] += score
        print(f"\nResult for query [{entered_query}]")
        rank = 0
        # Only return Top15
        for id_of_document in sorted(documents, key=documents.get, reverse=True):
            rank += 1
            if rank <= 15:
                score_output = format(documents[id_of_document], '.6f')
                print(f'{rank} {id_of_document} {score_output}')
            else:
                break
        query_end_time = time.process_time()
        query_time = query_end_time - query_start_time
        print(f"---------------------Execute Query Time: {query_time} sec.--------------------------------")
        entered_query = input('Enter query: ')


# This function can read the queries.txt
# Write the result in output.txt
# To enhance efficiency, in order to avoid calculated scores of terms repeatedly. For each query, I stored the unique token in the set.
def generate_output(term_index: dict):
    stemmer = porter.PorterStemmer()
    stopwords_set = get_stopwords()
    query_dict = dict()
    result_output = list()
    with open('./files/queries.txt', 'r') as lines:
        for line in lines:
            line = re.sub(r'[{}]+'.format(string.punctuation), '', line)
            line = line.lower()
            tokens = line.split()
            unique_tokens_set = set()
            query_id = tokens[0]
            query_dict[query_id] = dict()
            document_dict = query_dict[query_id]
            for term_query in tokens[1:]:
                if term_query not in stopwords_set:
                    if term_query not in stem_dict:
                        stem_dict[term_query] = stemmer.stem(term_query)
                    term_query = stem_dict[term_query]
                    if term_query not in unique_tokens_set:
                        unique_tokens_set.add(term_query)
                    else:
                        continue
                    if term_query in term_index:
                        for document_id, score in term_index[term_query]:
                            if document_id not in document_dict:
                                document_dict[document_id] = score
                            else:
                                document_dict[document_id] += score
            rank = 1
            for document_id in sorted(document_dict, key=document_dict.get, reverse=True):
                result_output.append((query_id, 'Q0', document_id, rank, document_dict[document_id], '19206197'))
                rank += 1
                if rank > 50:
                    break
    file = open('files/output.txt', 'w')
    for query_id, Q0, document_id, rank, score, UCD_id in result_output:
        score = format(score, '.4f')
        file.write(f"{query_id} {Q0} {document_id} {rank} {score} {UCD_id}")
        file.write('\n')
    file.close()


# This function is store each terms' documents BM25 score in a generated file named terms_small.txt
# Format: term  document_id  score
# It is an efficient way to generate BM25 index because system only need to calculate BM25 score in each documents for each terms appearing in query.
# So system store terms as the key the and put dictionary storing different documents score as value.
def generate_terms_file():
    # Judge whether this file has already existed, if it has been existed, system does not need to spend time to generate terms file again,
    # which could improve efficiency to some degree.
    if not os.path.isfile('./files/terms_small.txt'):
        terms, average_length, N, document_length = read_documents()
        for term in terms:
            document_score = list()
            for document_id, frequency in terms[term][1:]:
                document_cur_length = document_length[document_id]
                n_i = terms[term][0]
                # Use B25 Formula to calculate the score of each term
                score = (frequency * 2) / (
                            frequency + 0.25 + (0.75 * document_cur_length / average_length)) * math.log2(
                    (N - n_i + 0.5) / (n_i + 0.5))
                if score <= 0.0:
                    score = 0.0
                # Only six decimal places are displayed
                score = format(score, '.6f')
                document_score.append((document_id, score))
            terms[term] = document_score
        # Generate then write terms_small.txt file to store the score of term in each document
        file = open('./files/terms_small.txt', 'w')
        for term in terms:
            file.write(term + '\n')
            for document_id, score in terms[term]:
                file.write(document_id + ' ' + str(score) + '\n')
            file.write('   /\n')
        file.write('/')
        file.close()


# Based on Lab 7, I added a loop to calculate average score for various queries in different kinds of evaluation methods.
# I generated fifty results for each query, so the result is different from the output.txt result if relevant files' number exceed 50.
def execute_evaluation():
    # Some metrics in our evaluation system
    precision_sum = 0.0
    recall_sum = 0.0
    precision_10_sum = 0.0
    r_precision_sum = 0.0
    MAP_sum = 0.0
    bpref_score_sum = 0.0
    NDCG_sum = 0.0
    found_relevant = find_relevant_documents()
    found_retrieve = find_retrieved_documents()
    number_query = len(found_retrieve)
    print("Evaluation results:")

    # Precision & Recall Metrics Evaluation
    for query_id in found_retrieve:
        relevant_documents = found_relevant[query_id]
        relevant_documents_number = len(relevant_documents)
        retrieved_documents_number = len(found_retrieve[query_id])
        relevant_and_retrieved = 0
        for document in found_retrieve[query_id]:
            document_id = document[0]
            if document_id in relevant_documents:
                relevant_and_retrieved += 1
        precision = relevant_and_retrieved / retrieved_documents_number
        recall = relevant_and_retrieved / relevant_documents_number
        precision_sum += precision
        recall_sum += recall
    precision_score = precision_sum / number_query
    recall_score = recall_sum / number_query
    # Only four decimal places are displayed
    precision_score = format(precision_score, '.4f')
    recall_score = format(recall_score, '.4f')
    print(f"Precision: {precision_score}")
    print(f"Recall: {recall_score}")

    # Precision@10 Metrics Evaluation
    for query_id in found_retrieve:
        relevant_documents = found_relevant[query_id]
        relevant_and_retrieved = 0
        for document in found_retrieve[query_id][:10]:
            document_id = document[0]
            if document_id in relevant_documents:
                relevant_and_retrieved += 1
        precision_10 = relevant_and_retrieved / 10
        precision_10_sum += precision_10
    precision_10_score = precision_10_sum / number_query
    # Only four decimal places are displayed
    precision_10_score = format(precision_10_score, '.4f')
    print(f"P@10: {precision_10_score}")

    # R-precision Metrics Evaluation
    for query_id in found_retrieve:
        relevant_documents = found_relevant[query_id]
        relevant_documents_number = len(relevant_documents)
        relevant_and_retrieved = 0
        for document in found_retrieve[query_id][:relevant_documents_number]:
            document_id = document[0]
            if document_id in relevant_documents:
                relevant_and_retrieved += 1
        r_precision = relevant_and_retrieved / relevant_documents_number
        r_precision_sum += r_precision
    r_precision_score = r_precision_sum / number_query
    # Only four decimal places are displayed
    r_precision_score = format(r_precision_score, '.4f')
    print(f"R-precision: {r_precision_score}")

    # MAP Metrics Evaluation
    for query_id in found_retrieve:
        relevant_documents = found_relevant[query_id]
        relevant_documents_number = len(relevant_documents)
        relevant_and_retrieved = 0
        count = 1
        MAP_list = list()
        for document in found_retrieve[query_id]:
            document_id = document[0]
            if document_id in relevant_documents:
                relevant_and_retrieved += 1
                current_calculation = relevant_and_retrieved / count
                MAP_list.append(current_calculation)
            count += 1
        MAP_one_query = 0
        for item in MAP_list:
            MAP_one_query += item
        if relevant_documents_number != 0:
            MAP_one_query_score = MAP_one_query / relevant_documents_number
        else:
            MAP_one_query_score = 0
        MAP_sum += MAP_one_query_score
    MAP_final_result = MAP_sum / number_query
    # Only four decimal places are displayed
    MAP_final_result = format(MAP_final_result, '.4f')
    print(f"MAP: {MAP_final_result}")

    # bpref Metrics Evaluation
    # Because the small corpus does not have unjudged documents,
    # I only write and use the relevance judgments function in the system with large corpus.
    for query_id in found_retrieve:
        relevant_documents = found_relevant[query_id]
        relevant_documents_number = len(relevant_documents)
        N = 0
        bpref_sum = 0
        for document in found_retrieve[query_id]:
            document_id = document[0]
            if document_id in relevant_documents:
                score_of_one_query = 1 - N / relevant_documents_number
                bpref_sum += score_of_one_query
            else:
                N += 1
            if N == relevant_documents_number:
                break
        if relevant_documents_number != 0:
            bpref_one_query = bpref_sum / relevant_documents_number
        else:
            bpref_one_query = 0
        bpref_score_sum += bpref_one_query
    bpref_score = bpref_score_sum / number_query
    # Only four decimal places are displayed
    bpref_score = format(bpref_score, '.4f')
    print(f"bpref: {bpref_score}")

    # NDCG Metrics Evaluation
    for query_id in found_retrieve:
        relevant_documents = found_relevant[query_id]
        # print(relevant_documents)
        DCG = 0.0
        IDCG = 0.0
        for num, document in enumerate(found_retrieve[query_id][:10]):  # default is NDCG@10
            document_id = document[0]
            if document_id in relevant_documents:
                document_score = relevant_documents[document_id]
                # First and second calculation is special, could plus itself directly without division log calculation.
                if num < 2.0:
                    DCG += document_score
                else:
                    DCG += document_score / math.log2(num + 1.0)
        # ------------------------------------------------------------------------------------------------
        sorted_documents_list = sorted(relevant_documents.items(), key=lambda x: x[1], reverse=True)
        # print(sorted_documents_list)
        for num, document in enumerate(sorted_documents_list[:10]):
            document_score = float(document[1])
            if num < 2.0:
                IDCG += document_score
            else:
                IDCG += document_score / math.log2(num + 1.0)
        NDCG_sum += DCG / IDCG
    NDCG_score = NDCG_sum / number_query
    # Only four decimal places are displayed
    NDCG_score = format(NDCG_score, '.4f')
    print(f"NDCG: {NDCG_score}")


if __name__ == '__main__':
    #  Judge user's input in Terminal taking advantage of argarse package, then execute corresponding function in Terminal.
    parser = argparse.ArgumentParser(description='type')
    parser.add_argument('-m', default=False, help='python search_small.py -m')
    parser_parse_args = parser.parse_args()
    # Taking advantage of argarse to see the operation is "manual" or "evaluation"
    if parser_parse_args.m == "manual":
        write_start_time = time.process_time()
        generate_terms_file()
        write_end_time = time.process_time()
        write_time = write_end_time - write_start_time
        print(f"---------------------Read/Generate/Write File time: {write_time} sec.---------------------")
        build_index_start_time = time.process_time()
        terms = build_term_index()
        build_index_end_time = time.process_time()
        build_index_time = build_index_end_time - build_index_start_time
        print(f"---------------------Build Index of B25 time: {build_index_time} sec.----------------------------")
        execute_query(terms)
    elif parser_parse_args.m == "evaluation":
        overall_start_time = time.process_time()
        write_start_time = time.process_time()
        generate_terms_file()
        write_end_time = time.process_time()
        write_time = write_end_time - write_start_time
        print(f"---------------------Read/Generate/Write File Time: {write_time} sec.---------------------")
        build_index_start_time = time.process_time()
        terms = build_term_index()
        build_index_end_time = time.process_time()
        build_index_time = build_index_end_time - build_index_start_time
        print(f"---------------------Build Index of B25 Index Time: {build_index_time} sec.----------------------")
        generate_output(terms)
        execute_evaluation()
        overall_end_time = time.process_time()
        overall_time = overall_end_time - overall_start_time
        print(f"---------------------System Overall Run Time: {overall_time} sec.-------------------------")
    else:
        print('Hello! Please enter correct command to run the system :-)')
        print('Query manually command:  [python search_small.py -m manual]')
        print('Execute evaluation command:  [python search_small.py -m evaluation]')
