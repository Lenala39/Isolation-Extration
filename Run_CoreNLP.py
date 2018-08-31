import sys
import os
from os import walk
# for reading command line arguments
import argparse



def get_textfiles(folder):
    '''
    folder = folder in which the files to be parsed are in
    returns: a list of all txt files that are in the folder
    '''
    all_files = []
    txt_files = []
    # walk over folder and get all files
    for (dirpath, dirnames, filenames) in walk(folder):
        all_files.extend(filenames)
        break

    # check for all files if they are txt-files
    for file in all_files:
        if file.lower().endswith('.txt'):
            txt_files.append(file) #only append txt-files

    return txt_files

def run_script(files, filefolder, outputDir):
    '''
    files = list of files to run command on
    filefolder = folder the files are in (needed for specifying them in command)
    outputDir = output folder for xml files
    Runs core nlp for every single file
    '''

    for i in range(0,len(files)):
        # command from corenlp_students.sh
        # format with correct variable
        command = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,parse,depparse -file {}/{} -outputDirectory {}'.format(filefolder, files[i], outputDir)
        # execute command
        os.system(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', required=True, help='The folder of the txt files to run through coreNLP')
    parser.add_argument('--outputDirectory', required=True, help='The existing outputDirectory')
    args = parser.parse_args()

    folder = args.folder #folder with files is first (second) command line argument
    outputDir = args.outputDirectory # output Dir where XML files will be put

    txt_files = get_textfiles(folder) # get text files in that folder
    run_script(txt_files, folder, outputDir) #run script on those text files
