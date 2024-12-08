#read the file index.txt and prepare documents,vocab,idf

import chardet
def find_encoding(filename):
    r_file=open(filename,'rb').read()
    result=chardet.detect(r_file)
    charenc=result['encoding']
    return charenc

filename='Leetcode-Questions-Scrapper/index.txt'
my_encoding=find_encoding(filename)
with open(filename,'r',encoding=my_encoding) as f:
    lines=f.readlines()
    # print(lines)

#to preprocess the line like breaking the line into words 
def preprocess(document_text):
    # print(document_text)
    #remove the leading numbers in the text and make everything lowercase ,remove not alpha numeric characters
    terms=[term.lower() for term in document_text.strip().split()[1:] ]
    return terms

vocab={}
documents=[]
for index,line in enumerate(lines):
    # print(index,line)
    token=preprocess(line)
    documents.append(token)
    token=set(token)
    for tok in token:
        if tok not in vocab:
            vocab[tok]=1
        else:
            vocab[tok]+=1

#reverse sort the vocab the values
vocab=dict(sorted(vocab.items(),key=lambda x:x[1],reverse=True))

print("number of documents:",len(documents))
print("size of vocab",len(vocab))
print("sample document:",documents[0])
# print(vocab)

#save the vocab in a file
with open('tf-idf/vocab.txt','w') as f:
    for word in vocab.keys():
        f.write("%s\n" % word)

#save the idf values in a file
with open('tf-idf/idf-values.txt','w') as f:
    for word in vocab.keys():
        f.write("%s\n" % vocab[word])

#save the document in a file
with open('tf-idf/documents.txt','w') as f:
    for word in documents:
        f.write("%s\n" % ' '.join(word))

#inverted index
inverted_index={}
for index,document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token]=[index]
        else:
            inverted_index[token].append(index)

#save the inverted index in a text file
with open('tf-idf/inverted-index.txt','w') as f:
    for key in inverted_index.keys():
        f.write("%s\n" %key)
        f.write("%s\n" %' '.join([str(doc_id) for doc_id in inverted_index[key]]))
