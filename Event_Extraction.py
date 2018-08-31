import Event
from nltk import ParentedTree
import argparse
import Evaluation
from collections import Counter


def extract_substance(tree):
    '''
    extracts the substance that is isolated
    tree: sentence that describes the sentence
    returns: substance
    '''
    substance = ""
    # get the isolated component (= first NP)
    for complete_sentence in tree:
        for part_sentence in complete_sentence:
            if part_sentence.label() == "NP":
                substance = part_sentence.leaves()
    return substance


def extract_location(tree):
    '''
    extracts the location of isolation from a parse tree
    tree: tree to extract the source of the substance from
    returns: location
    '''
    location = ""
    com2_canidates = []

    # get all PPs because "from" is needed
    PPs = list(tree.subtrees(filter=lambda x: x.label()=='PP'))
    # get NPs inside the PP
    NPs_inside_PPs = list(map(lambda x: list(x.subtrees(filter=lambda x: x.label()=='NP')), PPs))
    for NPs in NPs_inside_PPs:
        # for every NP sentence in a PP
        for s in NPs:
            # check if the left siblig is a proposition (like from)
            if s.left_sibling() and s.left_sibling().label() =="IN":
                # store the content of the siblings
                words_temp = [w for w in s.leaves()]
                # if from is in the list
                if "from" in s.left_sibling().leaves():
                    # append the sibling of a "from"-node to the list we want
                    com2_canidates.append(' '.join(str(e) for e in words_temp))
    # remove duplicates
    com2_canidates = list(set(com2_canidates))
    location = com2_canidates
    return location

def extract_isolate(tree):
    '''
    extracts the substance and location of an isolation-event
    returns: event object
    '''
    substance = extract_substance(tree)
    location = extract_location(tree)
    #print("location in extract_isolate", location)
    #print("substance in extract_isolate", substance)
    event = Event.Event(substance, location)
    #print(event)
    return event

def batch_extract(file):
    '''
    extract the isolate event from the sentences in the txt files
    file: txt with (ROOT (S ...) ) sentences
    '''
    tree = ""
    events = []
    # open the input file with the sentences
    with open(file, "r") as file:
        # read a sentence
        sentence = file.readline()
        while sentence:
            sentence = sentence.strip("\n")
            try:
                # make a tree from the sentence
                tree = ParentedTree.fromstring(sentence)
                event = extract_isolate(tree)
                events.append(event)

            except Exception as e:
                pass

            sentence = file.readline()
    return events

def make_test_gold():
    '''
    handcrafted a gold set to test the evaluation methods
    :return: List of event objects
    '''
    gold_set_test = []

    p1s5 = Event.Event("Most of the ~30 known species of bifidobacteria",
                       ["the mammalian GIT,", "and some from the vaginal and oral cavity"])
    gold_set_test.append(p1s5)

    p1s10 = Event.Event("This strain", "infant feces")
    gold_set_test.append(p1s10)

    p2s6 = Event.Event("This strain", "an infected infant in Germany in 1993")
    gold_set_test.append(p2s6)

    p3s6 = Event.Event("This strain", "a patient with whooping cough")
    gold_set_test.append(p3s6)

    p4s2 = Event.Event("This species", ["a skin lesion", "a Lyme disease patient in Europe"])
    gold_set_test.append(p4s2)

    p5s3 = Event.Event("This organism", "Ixodes scapularis")
    gold_set_test.append(p5s3)

    p6s13 = Event.Event("Borrelia duttonii Ly", "a 2-year-old girl")
    gold_set_test.append(p6s13)

    p7s3 = Event.Event("The type strain of B. garinii", "Ixodes ricinus in France")
    p7s7 = Event.Event("This strain -LRB- OspA serotype 4 -RRB-",
                             "the cerebrospinal fluid of a patient with neuroborreliosis")
    p8s11 = Event.Event("Borrelia recurrentis", "adult patient with louse-borne relapsing fever in Ethiopia")
    p9s11 = Event.Event("This strain", "Glycine hispida in 1959 in Florida, USA,")
    p9s16 = Event.Event("Bradyrhizobium japonicum USDA 6", "soybean in Japan")
    gold_set_test.append(p7s3)
    gold_set_test.append(p7s7)
    gold_set_test.append(p8s11)
    gold_set_test.append(p9s11)
    gold_set_test.append(p9s16)
    return gold_set_test

def evaluate_results(parser_results, gold, edit_dist):
    '''
    evaluates the parser results against a gold standard
    :param parser_results: List of events from parser
    :param gold: List of events from gold standard
    :param edit_dist: edit distance that strings are allowed to differ
    :return: matches for component1, component2 and combined
    '''
    result_c1, result_c2 = Evaluation.compare(parser_results, gold_set, edit_dist)
    end_result = Evaluation.merge_lists(result_c1, result_c2)

    return result_c1, result_c2, end_result

def make_result_ouput(events, gold_set, edit_distances, print_sentences=True):
    '''
    creates the command line output of the comparison between the parser results and the gold set
    :param events: the parser results
    :param gold_set: the gold standard
    :param edit_distances: list of values what edit distances should be tried
    :param print_sentences: boolean to turn of the printing of the false/included sentences
    '''

    for i in edit_distances:
        result_c1, result_c2, end_result = evaluate_results(events, gold_set, i) # evaluate the results
        print("Edit distance: ", i)
        count_c1 = Counter(result_c1) # make counter object to add up values for True, False, Included
        count_c1.most_common()
        print("C1 results: ", count_c1)

        count_c2 = Counter(result_c2)
        count_c2.most_common()
        print("C2 results: ", count_c2)

        count_results = Counter(end_result)
        count_results.most_common()
        print("Results: ", count_results, "\n")

        # print all instances where result is not True to check mistakes the parser made
        if print_sentences is True:
            for i in range(0, len(end_result)):
                if end_result[i] is not "True":
                    print(end_result[i])
                    print("Expected: ", gold_set[i])
                    print("Got: ", events[i])
                    print("\n")
            print("\n \n")


if __name__ == '__main__':
    # extract the isolation-event from file:
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='The file with the sentences to extract the event from')
    parser.add_argument('--verbose', help='Whether or not the output should contain the false events in long form (True)')
    args = parser.parse_args()

    # events extracted
    events = batch_extract(args.file)
    # make a gold set
    gold_set = Evaluation.make_gold_set()
    # list of edit distances to try
    edit_distances = [0,1,2,7]

    # creates the command line output (can be piped into file)
    if args.verbose.lower() is "true":
        make_result_ouput(events, gold_set, edit_distances, True)
    else:
        make_result_ouput(events, gold_set, edit_distances, False)








