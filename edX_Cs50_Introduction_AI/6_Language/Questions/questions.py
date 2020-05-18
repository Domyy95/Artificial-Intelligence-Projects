import nltk
import sys
import math 
import os

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    mapping = {}

    for txt in os.listdir(directory):
        path = os.path.join(directory,txt)
        with open(path,encoding="utf-8") as f :
            mapping[txt] = f.read()

    return mapping

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    words = nltk.word_tokenize(document)

    rem = []

    for i in range(0,len(words)):
        words[i] = words[i].lower()

        if words in nltk.corpus.stopwords.words("english"):
            rem.append(i)
            continue 

    for i in rem:
        del words[i]
    
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    idf_values = {}

    for i in documents:

        cont = documents[i]

        for w in cont:

            if w in idf_values:
                continue

            else:
                count = 0
                total = 0

                for t in documents:

                    if w in documents[t]:
                        count +=1
                    
                    total += 1
                
                idf_values[w] = math.log(float(total/count))
        
        return idf_values


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    tf_idf = {}

    for f in files:
        sum = 0

        for w in query:

            idf = idfs[w]

            sum += files[f].count(w) * idf
        
        tf_idf[f] = sum
    
    rank = sorted(tf_idf.keys(), key = lambda x: tf_idf[x],reverse=True)
    rank = list(rank)

    try:
        return rank[0:n-1]
    except:
        return rank



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    idf = {}

    for s in sentences:
        sum = 0
        words = sentences[s]
        count = len(words)
        word_count = 0

        for w in query: 
            word_count = words.count(w)

            if w in words:
                sum += idf[w]
            
        idf[s] = (sum,float(word_count/count))
    
    rank = sorted(idf.keys(), key = lambda x: idf[x],reverse=True)
    rank = list(rank)

    try:
        return rank[0:n-1]
    except:
        return rank


if __name__ == "__main__":
    main()
