# for extracting the correct XML tag
import xml.etree.ElementTree as ET

# for execting bash/terminal code and accessing files in folder
import os
from os import walk

# for converting the (ROOT (NP ....)) notation to a diagram
from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

# for reading command line arguments
import argparse

# import Event class
import Event
import Event_Extraction


def extract(file):
    '''
    extracts the parse tags from the StanfordCoreNLP xml files
    and substitutes round for square brackets
    returns: parse: list of parsed sentences from file
    '''
    tree = ET.parse(file)
    root = tree.getroot()
    parse = []
    for sentences in root.findall('./document/sentences'):
        for sen in sentences.getchildren():
            for children in sen.getchildren():
                if(children.text.strip()):
                    #print(children.text.strip('\n'))
                    #print(children.text)
                    parse.append(children.text)

    return parse

def convert_round_brackets(parse):
    '''
    converts round to square brackets for online viewer
    '''
    for i in range(0, len(parse)):
        parse[i] = parse[i].replace("(", "[")
        parse[i] = parse[i].replace(")", "]")
    return parse

def xml_to_txt(folder, filter):
    '''
    creates an outfile with all the extracted parses from StanfordCoreNLP files
    folder: xml file folder
    filter: word that has to be in sentence
    '''
    all_files = []
    # walk over all files of the folder (which contains the xml files)
    for (dirpath, dirnames, filenames) in walk(folder):
        all_files.extend(filenames)
        break


    file_number = 0 #for the image name
    # for every xml file in the specified folder
    with open("out_test.txt", "w") as outfile:

        for file in all_files:
            file_number += 1
            path = folder + "/" + file #get the correct location for the file
            extracted_parse = extract(path) #extract the parse-tags

            if not filter:
                sentence_number = 0 # for the image name
                for sentence in extracted_parse:
                    sentence_number += 1
                    outfile.write(sentence)
                    outfile.write("\n")

            else:
                sentence_number = 0 # for the image name
                for sentence in extracted_parse:
                    sentence_number += 1
                    if filter in sentence:
                        outfile.write("\n")
                        outfile.write(sentence)


def xml_to_image(folder, outputDirectory, filter):
    '''
    writes all the extracted parse-tags into syntax trees
    folder = folder of the xml files to be parsed
    outputDirectory = directory the images will be saved to
    filter = word that has to be in sentence (optional)

    '''
    all_files = []
    # walk over all files of the folder (which contains the xml files)
    for (dirpath, dirnames, filenames) in walk(folder):
        all_files.extend(filenames)
        break


    file_number = 0 #for the image name
    # for every xml file in the specified folder

    for file in all_files:
        file_number += 1
        path = folder + "/" + file #get the correct location for the file
        extracted_parse = extract(path) #extract the parse-tags

        if not filter:
            sentence_number = 0 # for the image name
            for sentence in extracted_parse:
                sentence_number += 1
                make_tree_png(sentence, file_number, sentence_number, outputDirectory)

            #make_tree_png(extracted_parse[0], file_number, sentence_number, outputDirectory)

        else:
            sentence_number = 0 # for the image name
            for sentence in extracted_parse:
                sentence_number += 1
                if filter in sentence:
                    make_tree_png(sentence, file_number, sentence_number, outputDirectory)


def make_tree_png(sentence, file_number, sentence_number, outputDirectory):
    '''
    sentence: bracket notation of the sentence
    file_number: file the sentence originates from
    sentence_number: number of sentences
    outputDirectory: directory for the files (has to exist)
    Creates a png image with a syntax tree from the bracket notation of the given sentence
    '''
    filename = 'parse{}_sentence{}'.format(file_number, sentence_number)
    # make syntax tree using nltk
    cf = CanvasFrame()
    t = Tree.fromstring(sentence) # make tree from sentence
    tc = TreeWidget(cf.canvas(),t)
    cf.add_widget(tc,10,10) # (10,10) offsets
    cf.print_to_file('./{}/{}.ps'.format(outputDirectory, filename)) # print tree in a .ps file
    cf.destroy()

    # convert the ps files to usable (non-transparent) png images
    filepath = "./{}/{}".format(outputDirectory, filename)

    os.system('convert {}.ps {}.png'.format(filepath, filepath)) #convert to png
    os.system('convert -flatten {}.png {}.png'.format(filepath, filepath)) #make bg white
    os.system('del ".\{}\{}.ps"'.format(outputDirectory, filename)) #delete old .ps files


if __name__ == "__main__":
    # folder with xml files is the first command-line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', required=True, help='The folder of the xml files to parse')
    parser.add_argument('--outputDirectory', required=True, help='The existing outputDirectory')
    parser.add_argument('--filter', help='A word that has to be contained in the sentence to be outputted')
    args = parser.parse_args()

    # create either images or txt file from xml parsed files
    xml_to_image(args.folder, args.outputDirectory, args.filter)
    xml_to_txt(args.folder, args.filter)

