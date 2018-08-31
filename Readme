## Extraction of an "isolated-from"-event

Download the github directory to the local system. It is also necessary to have the [Stanford CoreNLP parser](https://stanfordnlp.github.io/CoreNLP/index.html#download) installed. 

#### Running the CoreNLP parser

In the directory of CoreNLP that also contains the input data, run the following commands:

	$ python Run_CoreNLP.py --folder=folder_of_input_txt --outputDir=dir_to_output_parses

The folder specifies the folder of the text files from the testing data set as input. The outputDir specifies the directory the resulting xml-files will be placed in. The result will be xml files created that lie in the outpurDir.

#### Extracting the parse-tags

Run the python-script in the folder you want to work in. The folder specifies where the xml files to be parsed are in. 
The output Directory is the directory, where the created tree images will be placed.
The filter is a word, that has to be in a sentence in order for it's tree to be generated.

	$ python Extract_Parse.py --folder=outputDir_with_xml_files --outputDir=dir_to_output_txt [--filter=word_to_filter]

The result will be a number of png-files in the outputDir and a file `out.txt` in the current directory, that contains the phrase structure parse from each sentence.

#### Extracting the events and evaluate them against a gold standard

To extract the events from the text-file containing the constituence parses (`out.txt`) run the following command:

	$ python Event_Extraction.py --file=txt_file --verbose=bool_for_verbosity

The -v-option specifies, whether or not the false parses should be printed in the output file. The output will be the printed evaluation results either in short or long form.