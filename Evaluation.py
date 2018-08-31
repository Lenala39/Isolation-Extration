import Event
import Levenshtein


def make_gold_set():
    '''
    handcrafted set of events from testing data
    empty if n.A. (better for comaprison with results)
    :return: list of gold-standard Event objects
    '''
    gold_standard = []

    p3s11 = Event.Event(component1="Bartonella tribocorum",
                        component2=["the blood of wild rats", "fleas obtained from wild rats"])
    p3s12 = Event.Event(component1="Bartonella elizabethae", component2="a case of endocarditis in a human")
    p3s14 = Event.Event(component1="This organism", component2="the blood of wild rats")

    p6s4 = Event.Event(component1="This species", component2="the feces of a breast-fed infant")

    p7s5 = Event.Event(component1="Most of the ~30 known species of bifidobacteria",
                       component2=["the mammalian GIT", "the vaginal and oral cavity"])

    p8s6 = Event.Event(component1="Most of the ~30 known species of bifidobacteria",
                       component2=["the mammalian GIT", "the vaginal and oral cavity"])
    p8s13 = Event.Event(component1="This strain", component2="human infant feces")

    p11s3 = Event.Event(component1=" ", component2=" ")
    p11s4 = Event.Event(component1="Burkholderia ambifaria AMMD",
                        component2="the rhizosphere of pea -LRB- Pisum sativum L. -RRB- near Arlington, Wisconsin, USA")

    p12s3 = Event.Event(component1="the reference strain, CH34",
                        component2="the sludge of a zinc decantation tank in Belgium that was polluted with high concentrations of several heavy metals")

    p13s12 = Event.Event(component1="Dehalococcoides sp. strain BAV1",
                         component2="PCE-to-ethene-dechlorinating microcosms established with aquifer material collected at the contaminated Bachman Road site in Oscoda, Michigan -LRB- 6-8, 13 -RRB-")

    p14s1 = Event.Event(component1="Desulfococcus oleovorans Hxd3",
                        component2="the saline water phase of an oil-water separator from a northern German oil field -LRB- 1,2 -RRB-")

    p16s8 = Event.Event(component1="D. deserti", component2="the Sahara desert")

    p17s3 = Event.Event(component1="the first strain of Tropheryma whipplei", component2=" ")

    p18s14 = Event.Event(component1="the genes", component2="in eukaryotes")

    p19s1 = Event.Event(component1="Thermoanaerobacter tengcongensis",
                        component2="a freshwater hot spring in Tengchong, China")

    p21s3 = Event.Event(component1="The sequenced strain", component2="Beppu hot spring in Japan")

    p22s1 = Event.Event(component1="Thermotoga maritima",
                        component2="geothermal heated marine sediment at Vulcano, Italy")

    p23s2 = Event.Event(component1="The organism, strain HB27",
                        component2="a natural thermal environment in Japan")

    p25s3 = Event.Event(component1="D. aromatica strain RCB", component2="Potomic River sediment, Maryland, USA")
    p25s31 = Event.Event(component1="Dechloromonas aromatica", component2=" ")
    p25s32 = Event.Event(component1="two unrelated strains, RCB and JJ,",
                         component2="two very diverse environments")

    p26s2 = Event.Event(component1="It", component2="soil contaminated with chlorinated industrial products")
    p26s5 = Event.Event(component1="D. restrictus", component2="a laboratory system that was being fed with tetrachloroethene")

    p27s11 = Event.Event(component1="The S. meliloti genome",
                         component2="nodules and soil primarily from host plants such as the Medicago -LRB- alfalfa and perennial and annual medics -RRB-, Melilotus -LRB- sweet clover -RRB-, and Trigonella -LRB- fenugreek -RRB- species -LRB- 11 -RRB-")
    p27s62 = Event.Event(component1=" ", component2=" ")

    gold_standard.append(p3s11)
    gold_standard.append(p3s12)
    gold_standard.append(p3s14)
    gold_standard.append(p6s4)
    gold_standard.append(p7s5)
    gold_standard.append(p8s6)
    gold_standard.append(p8s13)
    gold_standard.append(p11s3)
    gold_standard.append(p11s4)
    gold_standard.append(p12s3)
    gold_standard.append(p13s12)
    gold_standard.append(p14s1)
    gold_standard.append(p16s8)
    gold_standard.append(p17s3)
    gold_standard.append(p18s14)
    gold_standard.append(p19s1)
    gold_standard.append(p21s3)
    gold_standard.append(p22s1)
    gold_standard.append(p23s2)
    gold_standard.append(p25s3)
    gold_standard.append(p25s31)
    gold_standard.append(p25s32)
    gold_standard.append(p26s2)
    gold_standard.append(p26s5)
    gold_standard.append(p27s11)
    gold_standard.append(p27s62)

    return gold_standard


def compare(parser_results, gold_standard, edit_distance):
    '''
    Compares the parser results to the gold standard
    :param parser_results: list of event-parses from parser
    :param gold_standard: handcrafted events from gold standard
    :param edit_distance: can be set to account for small differences

    :return: two lists of strings "True", "Included" or "False"
    '''

    parser_c1 = [c1.component1 for c1 in parser_results]
    parser_c2 = [c2.component2 for c2 in parser_results]
    gold_c1 = [c1.component1 for c1 in gold_standard]
    gold_c2 = [c2.component2 for c2 in gold_standard]

    result_c1 = compare_component_list(parser_c1, gold_c1, edit_distance)
    result_c2 = compare_component_list(parser_c2, gold_c2, edit_distance)

    return result_c1, result_c2


def compare_component_list(parser_c, gold_c, edit_dist):
    '''
    compares two lists of items whether they are equal, one is included in the other or unequal
    :param parser_c: list of parser components
    :param gold_c: list of gold standard components
    :param edit_dist: whether small differences are false or true
    :return: list of strings with string-equality description
    '''
    result_list = []
    for i in range(0, len(parser_c)):
        if (parser_c[i] == gold_c[i]):
            result_list.append("True")

        elif (Levenshtein.distance(parser_c[i], gold_c[i]) <= edit_dist):
            result_list.append("True")

        elif (parser_c[i] in gold_c[i] or gold_c[i] in parser_c[i]):
            result_list.append("Included")

        else:
            result_list.append("False")

    return result_list


def compare_component_dict(parser_c, gold_c, edit_dist):
    '''
    same as compare_component_list but returns a dictionary with the values for True/False/Included
    :param parser_c:
    :param gold_c:
    :param edit_dist:
    :return: dict
    '''
    results = {"True": 0,
               "False": 0,
               "Included": 0
               }

    for i in range(0, len(parser_c)):
        if (parser_c[i] == gold_c[i]):
            results["True"] = results["True"] + 1
        elif (Levenshtein.distance(parser_c[i], gold_c[i]) <= edit_dist):
            results["True"] = results["True"] + 1

        elif (parser_c[i] in gold_c[i] or gold_c[i] in parser_c[i]):
            results["Included"] = results["Included"] + 1

        else:
            results["False"] = results["False"] + 1

    return results

def merge_lists(result_c1, result_c2):
    '''
    Merges the lists of each component
    True + True = True
    True + sth else = sth. else
    :param result_c1: compared list of component 1
    :param result_c2: compared list of component 2
    :return: list of end results
    '''
    end_result = []
    for i in range(0, len(result_c1)):
        if result_c1[i] == result_c2[i]:
            end_result.append(result_c1[i])
        elif result_c1[i] is "True" and result_c2[i] is not "True":
            end_result.append(result_c2[i])
        elif result_c2[i] is "True" and result_c1[i] is not "True":
            end_result.append(result_c1[i])
        else:
            end_result.append("False")
    return end_result


'''
   for i in range(len(parser_results)):
       print("sentence number", i)
       if (parser_results[i] == gold_standard[i]):
           print(True)
           results["True"] = results["True"] + 1

       elif (Levenshtein.distance(parser_results[i].component1,
                                  gold_standard[i].component1) <= edit_distance and Levenshtein.distance(
           parser_results[i].component1, gold_standard[i].component1) != 0):
           print("Almost true")
           print("Expected: ", end="")
           print(gold_standard[i])
           print("Result: ", end="")
           print(parser_results[i])
           results["Almost_true"] = results["Almost_true"] + 1


       elif (Levenshtein.distance(parser_results[i].component2,
                                  gold_standard[i].component2) <= edit_distance and Levenshtein.distance(
           parser_results[i].component2, gold_standard[i].component2)):
           print("Almost true")
           print("Expected: ", end="")
           print(gold_standard[i])
           print("Result: ", end="")
           print(parser_results[i])
           results["Almost_true"] = results["Almost_true"] + 1

       elif (parser_results[i].component1 in gold_standard[i].component1):
           print("Parse in gold standard at component 1")
           print("Expected: ", end="")
           print(gold_standard[i])
           print("Result: ", end="")
           print(parser_results[i])
           results["Included"] = results["Included"] + 1
       elif (gold_standard[i].component1 in parser_results[i].component1):
           print("Expected: ", end="")
           print(gold_standard[i])
           print("Result: ", end="")
           print(parser_results[i])
           results["Included"] = results["Included"] + 1

       elif (parser_results[i].component2 in gold_standard[i].component2):
           print("Expected: ", end="")
           print(gold_standard[i])
           print("Result: ", end="")
           print(parser_results[i])
           results["Included"] = results["Included"] + 1

       elif (gold_standard[i].component2 in parser_results[i].component2):
           print("Expected: ", end="")
           print(gold_standard[i])
           print("Result: ", end="")
           print(parser_results[i])
           results["Included"] = results["Included"] + 1

       else:
           print(False)
           print("Expected: ", end="")
           print(gold_standard[i])
           print("Result: ", end="")
           print(parser_results[i])
           results["False"] = results["False"] + 1
def compare_old(parser_results, gold_standard, edit_distance):
   bool_results = []
   for i in range(len(parser_results)):

       if (parser_results[i] == gold_standard[i]):
           bool_results.append(True)

       elif (Levenshtein.distance(parser_results[i].component1, gold_standard[i].component1) <= edit_distance):
           bool_results.append("Almost true")
           bool_results.append("Expected: ")
           bool_results.append(gold_standard[i].component1)
           bool_results.append("Result: ")
           bool_results.append(parser_results[i].component1)

       elif (Levenshtein.distance(parser_results[i].component2, gold_standard[i].component2) <= edit_distance):
           bool_results.append("Almost true")
           bool_results.append("Expected: ")
           bool_results.append(gold_standard[i].component2)
           bool_results.append("Result: ")
           bool_results.append(parser_results[i].component2)


       elif (parser_results[i].component1 != gold_standard[i].component1):
           if (parser_results[i].component1 in gold_standard[i].component1):
               bool_results.append("Parse in gold standard at component 1")
           elif (gold_standard[i].component1 in parser_results[i].component1):
               bool_results.append("Gold standard in parse at component 1")

       elif (parser_results[i].component2 != gold_standard[i].component2):
           if (parser_results[i].component2 in gold_standard[i].component2):
               bool_results.append("Parse in gold standard at component 2")
           elif (gold_standard[i].component2 in parser_results[i].component2):
               bool_results.append("Gold standard in parse at component 2")

       else:
           bool_results.append(False)

   return bool_results

   '''
