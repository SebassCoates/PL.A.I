import markovify
import sys
import json

"""GLOBAL VARIABLES (BECAUSE WE FOLLOW GREAT CODING CONVENTION)"""
dataset = "";
trainset_file = "";
training = False;
generating = False;
model_output_name = "";

"""ALL FUNCTIONS"""
def handleArgs():
        global dataset, trainset_file, training, generating 
        global model_output_name

        argv = sys.argv
        for arg in argv:
                if arg == "markovtrain.py":
                        pass
                elif "-train=" in arg:
                        if generating:
                                printExpectatedFormat()
                        jsonfile = arg.replace('-train=', '')
                        if jsonfile == "":
                                printExpectatedFormat()
                        else: 
                                model_output_name = jsonfile
                        training = True
                elif "-generate=" in arg:
                        if training:
                                printExpectatedFormat()
                        jsonfile = arg.replace('-generate=', '')
                        if jsonfile == "":
                                printExpectatedFormat()
                        else: 
                                trainset_file = jsonfile
                        generating = True
                elif ".json" in arg:
                        if training:
                                printExpectatedFormat()
                        trainset_file = arg
                elif ".mff" in arg:
                        if generating:
                                printExpectatedFormat()
                        processFile(arg)
                else:
                        printExpectatedFormat();

def processFile(filename):
        global dataset, trainset_file, training, generating;

        f = open(filename, 'r')
        dataset = dataset + f.read() + ".";

def printExpectatedFormat():
        print("Usage 1: -train=JSON_FILE_OUT_NAME filename [filenames]")
        print("Usage 2: -generate=JSON_FILE_IN_NAME")
        print("Train files must be formatted in .mff format")
        exit()

def trainChain(corpus):
        global model_output_name

        text_model = markovify.Text(corpus)
        
        model_json = text_model.to_json()

        writer = open(model_output_name, 'w')
        writer.write(model_json)


def generateOutput(json_file):
        f = open(json_file, 'r')
        json_filetext = f.read()

        loaded_model = markovify.Text.from_json(json_filetext)
        print(loaded_model.make_sentence())

"""MAIN FUNCTION - EXECUTED WHEN SCRIPT RUNS"""
def main():
        global training, generating, trainset_file
        handleArgs()
        if training:
                trainChain(dataset)
        else:
                generateOutput(trainset_file)

                        
if __name__ == "__main__":
    main()