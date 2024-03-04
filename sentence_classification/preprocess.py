from nltk import word_tokenize
from string import punctuation

from wbtools.lib.nlp.text_preprocessing import get_documents_from_text


def read_sentences_from_file(filepath, min_sent_length=20):
    return [sentence for line in open(filepath) for sentence in get_documents_from_text(
        sentences=[line.strip()], split_sentences=True) if len(sentence) > min_sent_length]

def read_sentences_from_file_with_papid(filepath, min_sent_length=20):
    return [(sent.strip().split("\t")[0], s[1].strip()) for sent in open(filepath) if len(s:=sent.split("\t")) > 1 and len(s[1]) > min_sent_length]

def clean_sentence(sentence):
    sentence = sentence.replace('/', ' / ')
    sentence = sentence.replace('.-', ' .- ')
    sentence = sentence.replace('.', ' . ')
    sentence = sentence.replace('\'', ' \' ')
    tokens = [token for token in word_tokenize(sentence) if token not in punctuation]
    sentence = ' '.join(tokens)
    sentence = sentence.strip(' ').strip('.;,/-|').strip()
    return sentence

def clean_sentences(sentences):
    return list(set([clean_sentence(sentence) for sentence in sentences]))

def clean_sentences_with_papid(sentences_with_papid):
    added_sentences = set()
    ret_sent = []
    for pap_id, sentence in sentences_with_papid:
        sentence = clean_sentence(sentence)
        if sentence not in added_sentences:
            added_sentences.add(sentence)
            ret_sent.append((pap_id, sentence))
    return ret_sent