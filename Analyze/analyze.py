from nltk.tokenize import sent_tokenize
import re
from string import digits
import sys


#Function: file_to_words
#input: file name, can be the path to file such as "/Users/chentong/Desktop/427/chentong-kim606-p2/part1/test.txt"
#output: a list or words
#assumption: words are string seperated by space in the file
def file_to_words(file_name):
    f = open(file_name, 'r').read().strip()
    word_list = [word for word in f.split()]
    return word_list

#test function     
#words = file_to_words("/Users/chentong/Desktop/427/chentong-kim606-p2/part1/part1_test_documents/readersdigest.txt")    
#print words
#print len(words)    

#function: file_to_clean_words
#input: file name, can be the path to file such as "/Users/chentong/Desktop/427/chentong-kim606-p2/part1/test.txt"
#output: a list of clean words
#assumption: clean words are strings only contain English Alphabat
def file_to_clean_words(file_name):
    f = open(file_name, 'r').read().strip()
    word_list = [word for word in re.split('\W+', f)]
    word_list = [word for word in word_list if word.isalpha()]
    return word_list

#test function     
#words = file_to_clean_words("/Users/chentong/Desktop/427/chentong-kim606-p2/part1/part1_test_documents/readersdigest.txt")    
#print words
#print len(words)

#Function: file_to_sent
#input: file name, can be the path to file 
#output: a list of sentences from file
def file_to_sent(file_name):
    f = open(file_name, 'r').read().strip()
    f = unicode(f, 'utf-8')
    return sent_tokenize(f)

#test
#a = file_to_sent("/Users/chentong/Desktop/427/chentong-kim606-p2/part1/part1_test_documents/gettysburg.txt")
#b = file_to_sent("/Users/chentong/Desktop/427/chentong-kim606-p2/part1/part1_test_documents/nytimes.txt")

#function letter_count
#input: list of clean words (output of file_to_clean_word)
#output: number of letters in the list
#assumption: letters are symbols in alphabet (a-z, A-Z)
def letter_count(clean_word_list):
    s = "".join(clean_word_list)
    return len(s)

#test     
assert letter_count(["hhh","happy", "hello", "world"]) == 18
assert letter_count(["happy", "hello", "world"]) == 15

#function: word_count
#input: a list of words (output of file_to_words)
#output: number of words in the list
def word_count(word_list):
    return len(word_list)

#test     
assert word_count(["hhh","happy", "hello", "world"]) == 4


#This function takes a list of sentences (output of file_to_sentences)
#returns the number of sentences
def sent_count(sent_list):
    return len(sent_list)

#test     
#sent_list = file_to_sent("part1_test_documents/nytimes.txt")
#output = word_count(sent_list)

#This functions takes a string
#returns the number of syllables in the string
def syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    #scan through word to look for vowels which is not followed by a vowel
    for i in range (len(word) - 1):
        if word[i] in vowels and word[i+1] not in vowels:
           count += 1
    #scan the last letter in word
    last = word[len(word)-1]
    if last in vowels and (last != 'e' or count == 0):
        count += 1
    return count

#test
assert syllables("apple") == 1
assert syllables("happy") == 2
assert syllables("create") == 1

#Function: syllables_count
#input: a list of clean word
#output: sum of syllables of each words
def syllables_count(word_list):
   return sum(map(lambda x : syllables(x), word_list))

#test
assert syllables_count(["apple", "nice", "happy", "learn"]) == 5
assert syllables_count(["greate", "grange", "make", "eat","assignment"]) == 7

#Coleman-Liau index
def cl_score (letter_count, word_count, sent_count):
    return round(5.88 * letter_count/word_count - 29.6 * sent_count/word_count - 15.8, 2)

#test
assert cl_score(7000,600,60) == 49.84

#Flesch-Kincaid score
def fk_score(word_count, sent_count, syll_count):
    return round(0.39 * word_count/sent_count + 11.8 * syll_count/word_count - 15.59, 2)

#test
assert fk_score(7000,600,90000) == 140.67


if __name__ == "__main__":
    file_name = sys.argv[1]
    print "Analyzing test_documents/" + file_name + "..."
    word_list = file_to_words(file_name)
    clean_word_list = file_to_clean_words(file_name)
    sent_list = file_to_sent(file_name)
    words = word_count(word_list)
    sents = sent_count(sent_list)
    letters = letter_count(clean_word_list)
    sylls = syllables_count(clean_word_list)
    print "Number of words: " + str(words)
    print "Number of sentences: " + str(sents)
    print "CL level: " + str(cl_score(letters, words, sents))
    print "Total number of syllables: " + str(sylls)
    print "FK level: " + str(fk_score(words, sents, sylls))

