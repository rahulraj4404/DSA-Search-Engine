import math 
import time

def load_vocab():
    vocab={}
    with open('tf-idf/vocab.txt','r') as f:
        vocab_terms=f.readlines()
    with open('tf-idf/idf-values.txt','r') as f:
        idf_values=f.readlines()
    for (term,idf_value) in zip(vocab_terms,idf_values):
        vocab[term.strip()]=int(idf_value.strip()) 
    return vocab


def load_documents():
    documents=[]
    with open('tf-idf/documents.txt','r') as f:
        documents=f.readlines()
    documents=[document.strip().split() for document in documents]  
    print("no of documents",len(documents))
    print("sample documents",documents[0])
    return documents


def load_inverted_index():
    inverted_index={}
    with open('tf-idf/inverted-index.txt','r') as f:
        inverted_index_terms=f.readlines()
    for row_num in range(0,len(inverted_index_terms),2):
        term=inverted_index_terms[row_num].strip()
        documents=inverted_index_terms[row_num+1].strip().split()
        inverted_index[term]=documents
    print('size of inverted index:',len(inverted_index))
    return inverted_index

# def load_links():
#     links=[]
#     with open('Leetcode-Questions-Scrapper/Qindex.txt','r') as f:
#         links=f.readlines()
#     links=[link.strip() for link in links]
#     return links

vocab_idf_values=load_vocab()
documents=load_documents()
inverted_index=load_inverted_index()
# links=load_links()


def get_tf_dictionary(term):
    tf_values={}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document]=1
            else:
                tf_values[document]+=1
    for document in tf_values:
        tf_values[document]/=len(documents[int(document)])
    return tf_values

def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term])



def calculate_sorted_order_of_documents(query_terms):
    start_time=time.time()
    potential_documents={}
    for term in query_terms:
        if vocab_idf_values[term] == 0:
            continue
        tf_values_by_document=get_tf_dictionary(term)
        idf_value=get_idf_value(term)
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document]=tf_values_by_document[document]*idf_value
            potential_documents[document]+=tf_values_by_document[document]*idf_value

    #divide the length of the query terms
    for document in potential_documents:
        potential_documents[document]/=len(query_terms)

    potential_documents=dict(sorted(potential_documents.items(),key=lambda item:item[1],reverse=True))
    end_time=time.time()
    search_duration=end_time-start_time
    print(f"Search completed in {search_duration:.6f} seconds.")
    # print(potential_documents)
    for document_index in potential_documents:
        print('Document: ',documents[int(document_index)],'Score: ',potential_documents[document_index])
    # return potential_documents
    # end_time=time.time()
    # search_duration = end_time - start_time
    # print(f"Search completed in {search_duration:.6f} seconds.")




query_string=input("enter your query: ")

query_terms=[term.lower() for term in query_string.strip().split()]

print(query_terms)
calculate_sorted_order_of_documents(query_terms) 

# def search(query, documents, vocab_idf_values, inverted_index,links):
#     query_terms = [term.lower() for term in query.strip().split()]
#     potential_documents = calculate_sorted_order_of_documents(query_terms)
#     results = [{'title': f'Document {doc_id}', 'link': links[int(doc_id)], 'score': potential_documents[doc_id]} for doc_id in potential_documents]
#     return results