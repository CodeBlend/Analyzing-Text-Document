from collections import Counter
import math
import re
from string import digits
import sys
from sets import Set

#Function: nice_word_list
#input: file name, can be the path to file such as "/Users/chentong/Desktop/427/chentong-kim606-p2/part12/test.txt"
#output: a list of nice word from file
#nice word means
#--- no puctuations
#--- all lower case
#--- no number
#--- most of non sense string remove (such as "this" "that")
#--- string lenth longer than 2

def nice_word_list(file_name):
    f = open(file_name, 'r').read().strip()
    f = f.lower()
    word_list = [word for word in re.split('\W+', f)]
    #remove all numbers, non sense words and all words less <=2 letters long
    non_sense = set(["this", "that", "are", "and", "the", "for"])
    word_list = [word for word in word_list if word not in non_sense and len(word) > 2 and word.isalpha()]
    return word_list
#test
#print nice_word_list("/Users/chentong/Desktop/427/chentong-kim606-p2/part2/part2_train/health")


#Function: count_occur
#inputs: a string word and a list of string words
#output: integer as number of times word occurs in words
def count_occur(word, words):
    counts = map(lambda x : 1 if x == word else 0, words)
    return sum(counts)

#test
assert count_occur("chen", ["chen", "thinks", "I427", "has", "too", "much", "homework"]) == 1


#Function measure
#input: test_doc -- a list of nice word from the doucment we want to evaluate
#       test_cata -- list of nice words from the catagory we want to evaluate
#       catas  -- list of list of nice words from all the catagories from training set
#output: score -- a float calcuated based on Bayesian classier
#        contribution -- a dictionary records the score contribution of 5 words with highest contribution

def measure(test_doc, test_cata, catas):
    score = 0
    contribution = {}

    for word in test_doc:
        count_in_test = count_occur(word, test_cata)
        count_in_other = sum(map(lambda x : count_occur(word, x), catas))

        if count_in_test == 0 and count_in_other != 0:
            this_score = -1 * math.log(count_in_other, 2)

        if count_in_test != 0 and count_in_other == 0:
            this_score = math.log(count_in_test, 2)

        if count_in_test != 0 and count_in_other != 0:
            this_score = math.log(count_in_test, 2) - math.log(count_in_other, 2)

        score += this_score

        if word in contribution:
            contribution[word] += this_score
        else:
            contribution[word] = this_score

    return score, Counter(contribution).most_common()[:5]

#test
t = ["world", "hello", "hello"]
test_cata = ["hello", "hello", "world"]
catas = [["chen", "hello"], ["hi","hello"], ["hello"]]
score, con = measure(t, test_cata, catas)
assert score == math.log(1,2) + math.log(2,2) - math.log(3,2) + math.log(2,2) - math.log(3,2) 

#function for printing most informative words in document
def print_contribution(con):
    print "The most informative words in this document were:"
    for item in con:
        print "- " + item[0] + "    " + str(item[1])

if __name__ == "__main__":

    file_name = sys.argv[1]
    print "Evaluating the " + file_name + "..."
    test_list = nice_word_list(file_name)
    categories = ["business", "entertainment", "health", "scitech", "sports", "world"];
    business = nice_word_list("part2_train/"+ categories[0])
    entertainment = nice_word_list("part2_train/" + categories[1])
    health = nice_word_list("part2_train/" + categories[2])
    scitech = nice_word_list("part2_train/" + categories[3])
    sports = nice_word_list("part2_train/" + categories[4])
    world = nice_word_list("part2_train/" + categories[5])

    business_score, business_con = measure(test_list, business, [entertainment, health, scitech, sports, world])
    entertainment_score, entertainment_con = measure(test_list, entertainment, [business, health, scitech, sports, world])
    health_score, health_con = measure(test_list, health, [business, entertainment, scitech, sports, world])
    scitech_score, scitech_con = measure(test_list, scitech, [business, entertainment, health, sports, world])
    sports_score, sports_con = measure(test_list, sports, [business, entertainment, health, scitech, world])
    world_score, world_con = measure(test_list, world, [business, entertainment, health, scitech, sports])
    
    print "Score for category:"
    print "- business: " + str(business_score)
    print "- entertainment: " + str(entertainment_score)
    print "- scitech: " + str(scitech_score)
    print "- sports: " + str(sports_score)
    print "- world: " + str(world_score)

    max_score = max(business_score, entertainment_score, health_score, scitech_score, sports_score, world_score)

    if max_score == business_score:
        print "The document's category is most likely: business"
        print_contribution(business_con)

    if max_score == entertainment_score:
        print "The document's category is most likely: entertainment"
        print_contribution(entertainment_con)
        
    if max_score == health_score:
        print "The document's category is most likely: health"
        print_contribution(health_con)

    if max_score == scitech_score:
        print "The document's category is most likely: scitech"
        print_contribution(scitech_con)

    if max_score == sports_score:
        print "The document's category is most likely: sports"
        print_contribution(sports_con)

    if max_score == world_score:
        print "The document's category is most likely: world"
        print_contribution(world_con)
