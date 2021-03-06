# Type-Token Calculator.py
import re
import os
import sys
import datetime
import csv
from chardet import UniversalDetector
# import docx

detector = UniversalDetector()
reader_dict = {}

##############################
# Defining custom Exceptions #
##############################

class BadFilenameException(Exception):
    """ Exception raised when the structure of the filename cannot support the
        naming convention required by our program and analysis.
    """
    pass

class EmptyFileException(Exception):
    """ Exception raised when the file is empty.
    """
    pass

class FileTooShortException(Exception):
    """ Exception raised when the file does not have the required content.
        Specifically, the file has too few lines, suggesting it only has headers
        and not content.
    """
    pass

###############################################
# Defining a class for Leveled Reader objects #
###############################################

class LeveledReader():
    leveled_reader_ct = 0

    def __init__(self, id, title, author, page_ct, word_ct,
                 tt_ratio, type_ct, token_ct, unique_words, words,
                 word_len_char="not calculated",
                 sent_len_word="N/A"):
        """Initialize instance of Leveled Reader book"""
        LeveledReader.leveled_reader_ct += 1
        self.id = id
        self.title = title
        self.author = author
        self.page_ct = page_ct
        self.word_ct = word_ct
        self.tt_ratio = tt_ratio
        self.type_ct = type_ct
        self.token_ct = token_ct
        self.unique_words = unique_words
        self.words = words
        self.word_len_char = word_len_char
        self.sent_len_word = sent_len_word
        self.content = {}
        for page in range(0, page_ct):
            self.content.update(page = "")

############################################
# Functions needed to execute this program #
############################################

def process_reader(reader_file, verbosity):
    """ Function to create a LeveledReader object from a
        file in your filesystem.

        Function takes two inputs:
            reader_file (str) - name of the file that will be processed;
                has the format 'LR-#-{ENG/KIS}-{A-J}-{CODE}-TITLE.AUTHOR'
            verbosity (str) - how much output you expect as the function runs

    """
    # Open file, read in contents
    # try:
    # fh = open(reader_file, mode="r", encoding="UTF-8")
    # fh = open(reader_file, mode="r", encoding="UTF-16")
    encodingcheck = open(reader_file, mode="rb").read()
    print(f"The file being examined is {reader_file}")
    detector.reset()
    detector.feed(encodingcheck)
    print(detector.close())
    enc_result = detector.close()["encoding"]
    print(f"This file will be read using {enc_result} encoding")
    fh = open(reader_file, mode="r", encoding=enc_result)
    # print(chardet.detect(fh))
    # except:
    #     print("The file was not encoded as UTF-8. Now attempting UTF-16.")
    #     fh = open(reader_file, mode="r", encoding="UTF-16")
    filename = fh.name.split("-")
    if not len(filename) == 6:
        print("*" * 126)
        print("The filename {} is malformed; the file will be skipped.\n".format(fh.name))
        print()
        print("*" * 126)
        # raise BadFilenameException
        return None
    reader_id = filename[4] # Uses the unique code generated by Brenda et al
    data = fh.readlines()
    # print(data)
    if len(data) == 0:
        print("*" * 126)
        print("The file {} is empty. Proceeding to the next.\n".format(fh.name))
        print()
        print("*" * 126)
        # raise EmptyFileException
        return None
    elif len(data) < 4:
        print("*" * 126)
        print("The file {} is incomplete. Proceeding to the next.\n".format(fh.name))
        print()
        print("*" * 126)
        # raise FileTooShortException
        return None
    print("-" * 126)
    print("Analyzing {}.\n".format(fh.name))
    # Initialize counters, dicts, etc.
    curr_line = 0
    reader_word_ct = 0
    reader_type_dict = {}
    # Define a RegEx substitution pattern to eliminate punctuation we wish to
    # ignore
    pattern = re.compile("[0-9.,:;\-\—?!“”_…\"’‘]*")
    # Process the contents of the -reader_file-
    for line in data:
        line = re.sub(pattern, "", line).lower()
        words = line.split()
        if curr_line == 0:
            level_expected = words[1]
        elif curr_line == 1:
            reader_title = " ".join(words[:]).capitalize()
        elif curr_line == 2:
            reader_author = " ".join(w.capitalize() for w in words[:])
        else:
            new_word_ct = 0
            new_word_lst = []
            page_word_ct = 0
            if verbosity == "p":
                print("\tAs of page {}, new word ct is {}...".format(curr_line - 2, new_word_ct))
            for word in words:
                page_word_ct += 1
                if word not in reader_type_dict.keys():
                    new_word_ct += 1
                    new_word_lst.append(word)
    #             print(word, new_words,":",book_types_dict.keys())
                reader_type_dict[word] = reader_type_dict.get(word, 0) + 1
            reader_word_ct += page_word_ct
            reader_type_ct = len(reader_type_dict.keys())
            reader_token_ct = sum(reader_type_dict.values())
            if reader_token_ct != 0:
                reader_type_token_ratio = reader_type_ct/reader_token_ct
            else:
                reader_type_token_ratio = 9999
            if verbosity == "p":
                print("\tPage {}'s {} total words included {} new words: ({})\n".format(curr_line - 2, page_word_ct, new_word_ct, new_word_lst) +
                  "\t\tTTR is now {:.2f} ".format(reader_type_token_ratio) +
                  "(from {} / {})".format(reader_type_ct, reader_token_ct))
        curr_line += 1

    reader_page_ct = curr_line - 1 # B/c incremented at end of loop
    reader_unique_words = list(reader_type_dict.keys())

    # Define the attributes that will be required in order to generate the
    # LeveledReader object
    reader_attribs = [reader_id, reader_title, reader_author, reader_page_ct,
                      reader_word_ct, reader_type_token_ratio, reader_type_ct,
                      reader_token_ct, reader_unique_words, reader_type_dict]

    # Store the new LeveledReader object in a dict so we can retrieve them all
    # To-Do: Update so there's a test of whether the LRObject is already in the
    # dict; if so, insert using a modified id (e.g. 999b, 999c, etc.)
    reader_dict[reader_id] = LeveledReader(*reader_attribs)
    print()
    print("Analysis of '{}' by {} completed.".format(reader_title, reader_author))
    print("It is expected to be a Level {} book with {} pages and an ".format(level_expected.upper(), curr_line - 3) +
          "overall type-token ratio of {:.2f}".format(reader_type_token_ratio))
    if verbosity == "p":
        print("This is derived from a total word count of {} with the ".format(reader_word_ct) +
              "following {} unique words: ".format(reader_type_ct))
        print()
        print("+" * 126)
        print()
        # for u_word in book_types_dict.keys():
            # print(u_word, ", ", end="")
        rows = len(reader_unique_words) // 8
        # print("Printing out the unique words will require {} rows".format(rows))
        first_word = 0
        if rows >= 1:
            for r in range(0, rows):
                # print("Now printing words from {}:{}".format(first_word, first_word + 8))
                words_to_print = reader_unique_words[first_word:(first_word + 8)]
                print("[{:=2}] ".format(r + 1) +
                      "{:<15}{:<15}".format(words_to_print[0],words_to_print[1]) +
                      "{:<15}{:<15}".format(words_to_print[2],words_to_print[3]) +
                      "{:<15}{:<15}".format(words_to_print[4],words_to_print[5]) +
                      "{:<15}{:<15}".format(words_to_print[6],words_to_print[7]) +
                      "{:>}".format("+"))
                if r == (rows - 1):
                    # first_word += 0
                    first_word += 8
                    # print("On last row {}; first_word is now {}".format(r, first_word))
                else:
                    first_word += 8
                    # print("On row {}; first_word is now {}".format(r, first_word))
            remainder_words = reader_unique_words[first_word:]
            print("[{:=2}] ".format(r + 2), end="")
            for r_word in remainder_words:
                print("{:<15}".format(r_word), end="")
        else:
            print("[ 1] ", end="")
            for u_word in reader_unique_words:
                print("{:<15}".format(u_word), end="")
        print("\n")
        print("+" * 126)
        print("\n")


def get_dir_and_file(running_mode):
    """ Function to get input from the user"""
    print("-" * 126)
    print()
    print("Please provide the directory in which your files are stored")
    lr_dir = input("\t >>: ")
    print()
    exit_ttr() if lr_dir == "q" else lr_dir
    backslash = re.compile(r"\\")
    lr_dir = re.sub(backslash, "/", lr_dir)
    os.chdir(lr_dir)
    file_list = []          # Will need to move this outside of the command in order to have a persistent file list...
    if running_mode == "m":
        print("-" * 126)
        print()
        print("Which file would you like to process at this time?:")
        f = input("\t >>: ")
        print()
        # print(os.path.join(lr_dir, f), "<-- The file to be processed...")
        file_list.append(f) if os.path.isfile(os.path.join(lr_dir, f)) else file_list
    elif running_mode == "a":
        print("-" * 126)
        print()
        print("Thank you. Please provide the file extension (format) of the " +
              "files you intend to process. \n\te.g. .docx, .txt, .csv, .xlsx")
        lr_ftype = input("\t >>: ")
        print()
        exit_ttr() if lr_ftype == "q" else lr_ftype
        file_list = [f for f in os.listdir(lr_dir) if os.path.isfile(
                                                    os.path.join(lr_dir, f))
                                                    and f.endswith(lr_ftype)]
    print("-" * 126)
    print()
    print("This function will run on the following files:")
    confirmation, file_list = verify_file_list(file_list)
    print()
    exit_ttr() if confirmation == "q" else confirmation
    if confirmation == "c":
        print("Thank you. We'll proceed. \n")
    return file_list

#############################
# User Interaction Function #
#############################
def user_interaction():
    """ Function to govern user interaction, including obtaining the
        preferred -running_mode- and -verbosity-, and calling the
        -get_dir_and_file- function
    """
    print("-" * 126)
    print()
    print("Would you like to [m]anually enter filenames, or " +
          "would you prefer to let this run in [a]utomated mode?")
    running_mode = input("\t >>: ").lower()
    print()
    while running_mode not in "maq":
        running_mode = input_nudge("user")
        print("." * 126)
        print("\n")
    if running_mode == "q":
        print("Thank you for using Type-Token Calculator. Good-bye.")
        sys.exit()
    print("-" * 126)
    print()
    print("Would you like the routine to [p]rint out the specs for each book as " +
          "it goes, or would you prefer to let this run [s]ilently?")
    verbosity = input("\t >>: ").lower()
    print()
    while verbosity not in "psq":
        verbosity = input_nudge("verbosity")
        print("." * 126)
        print("\n")
    if verbosity == "q":
        print("Thank you for using Type-Token Calculator. Good-bye.")
        sys.exit()
    return running_mode, verbosity

def verify_file_list(file_list):
    """ Function to nicely print out the current file list through which
        the -process_reader- function will loop.
    """
    print()
    print("~" * 126)
    print_file_list(file_list)
    print("Please [c]onfirm the list is accurate. If there are any files you " +
            "want to [r]emove from the list, now is the time.")
    confirmation = input("\t >>: ").lower()
    print()
    while confirmation not in "rc":
        confirmation = input_nudge("verify")
        print()
    if confirmation == "r":
        file_to_drop = ""
        while file_to_drop is not "f":
            print("-" * 126)
            print()
            print("Please provide the number for the file you wish to remove.\n" +
                  "When you have [f]inished, please enter 'f'.")
            file_to_drop = input("\t >>: ")
            print()
            if re.match("[0-9]+", file_to_drop):
                removed = file_list.pop(int(file_to_drop) - 1)
                print("{} removed.".format(removed))
                print_file_list(file_list)
        if file_to_drop == "f":
            confirmation = "c"
    return confirmation, file_list

def print_file_list(file_list):
    """ Function to nicely print out the current file list through which
        the -process_reader- function will loop.
    """
    file_num = 0
    for f in file_list:
        file_num += 1
        print("[{:>2}]\t{}".format(file_num, f))
    print("~" * 126)
    print()

def exit_ttr():
    """Function to gracefully exit the Type-Token Ratio calculator
    """
    print("Thank you for using Type-Token Calculator. Good-bye.")
    sys.exit(1)

def input_nudge(sending_routine):
    """ Routine to remind the user of their input options.
    """
    print("." * 126)
    print("Sorry, that input was not understood. To recap, valid inputs are")
    if sending_routine == "proc_comp":
        print("\t[c] for 'continue' (new story or directory)\n" +
              "\t[f] for 'finish' (export results and close out of the " +
              "Type-Token Ratio Calculator")
    elif sending_routine == "verify":
        print("\t[c] for 'confirm' (that all files listed are to be analyzed)\n" +
              "\t[r] for 'remove' (to remove a file from the list provided)")
    elif sending_routine == "user":
        print("\t[m] for 'manual' mode (provide--and analyze--files one at " +
              "a time)\n" +
              "\t[a] for 'automatic' mode (provide a directory containing a " +
              "batch of files to analyze)")
    elif sending_routine == "verbosity":
        print("\t[p] for 'print' mode (reports updated figures for each page " +
              "during the analysis)\n" +
              "\t[s] for 'silent' mode (reports only the TTR at the end of " +
              "each analysis)")
    elif sending_routine == "output_fname":
        print("\t[a] to 'accept' the default filename\n" +
              "\t[c] to 'choose' a different filename")
    elif sending_routine == "output_dname":
        print("\t[a] to 'accept' the current output directory\n" +
              "\t[c] to 'choose' a different output directory")
    print("\t[q] for 'quit' (to quit the Type-Token Ratio Calculator without " +
          "writing the results to file)")
    new_command = input("\t >>: ").lower()
    exit_ttr() if new_command == "q" else new_command
    return new_command

def processing_complete(running_mode):
    """ Routine to run when file processing has completed.
    """
    print("Analysis of the following stories has been completed: ")
    print_file_list(file_list)
    # if running_mode == "m":
    #     prompt = "story"
    # elif running_mode == "a":
    #     prompt = "directory"
    prompt = "story" if (running_mode == "m") else "directory" #if (running_mode == "a") else ""
    print("Would you like to [c]ontinue with a new {}, or\n".format(prompt) +
          "would you like to [f]inish and export your analyses?")
    next_task = input("\t >>: ").lower()
    print()
    while next_task not in "cfq":
        input_nudge("proc_comp")
        next_task = input("\t >>: ").lower()
        print()
    if next_task == "f":
        output_to_file(reader_dict)
        proceed = False
    elif next_task == "c":
        proceed = True
    elif next_task == "q":
        exit_ttr()
    return proceed

def output_to_file(dict_of_readers):
    """ Function to output the contents of the dict containing the leveled
        reader analysis to a .csv file

        Takes as input a dictionary rile

    Arguments:
        dict_of_readers {dict} -- k: reader IDs, v: LeveledReader Objects
    """
    print("." * 126)
    print()
    date = datetime.datetime.now()
    date_str = "{:0>4}-{:0>2}-{:0>2}".format(date.year, date.month, date.day)
    destination_fname = "TTR Report {}.csv".format(date_str)
    print("By default, the output will be saved to '{}'".format(destination_fname))
    print("Please [a]ccept the default or [c]hoose a new filename.")
    accept_default_fname = input("\t >>: ").lower()
    while accept_default_fname not in "ac":
        accept_default_fname = input_nudge("output_fname")
    if accept_default_fname == "c":
        destination_fname = input("\t >>: ")
    print(destination_fname[-1:-5],"<-- end of the filename")
    destination_fname += ".csv" if (destination_fname[-4:] != ".csv") else ""
    destination_dir = os.getcwd()
    print("Your current working directory is \n\t'{}'".format(destination_dir))
    print("By default, the output will be saved to the current working directory.")
    print("Please [a]ccept the default or [c]hoose a new destination directory.")
    accept_default_destination = input("\t >>: ")
    while accept_default_destination not in "ac":
        accept_default_destination = input_nudge("output_dname")
    if accept_default_destination == "c":
        print("Please provide the directory in which you would like your report.")
        destination_dir = input("\t >>: ")
        while not os.exists(destination_dir):
            print("Sorry, that directory is not found.")
            destination_dir = input("\t >>: ")
    full_path = os.path.join(destination_dir, destination_fname)
    backslash = re.compile(r"\\")
    full_path = re.sub(backslash, "/", full_path)
    print("You have supplied '{}'".format(full_path))
    while os.path.isfile(full_path):
        print("That directory and filename already exist. To avoid overwriting " +
              "an existing report the filename will be changed.")
        increment = 0
        full_path = full_path[:-4] + "." + str(increment) + ".csv"
        increment += 1
    # try:
    with open(full_path, "w", newline="") as csvfile:
        lro_attribs = list(vars(dict_of_readers[list(dict_of_readers.keys())[0]]).keys())
        remapping_dict = {'id': "Reader ID",
                          'title': "Title",
                          'author': "Author",
                          'page_ct': "Page Ct",
                          'word_ct': "Word Ct",
                          'type_ct': "Type Ct",
                          'token_ct': "Token Ct",
                          'word_len_char': "Avg Length of Words (# Chars)",
                          'sent_len_word': "Avg Length of Sentences (# Words)",
                          'content': "Content",
                          'words': "Words w Counts",
                          'unique_words': "Unique Words",
                          'tt_ratio': "Type-Token Ratio"}
        columns = [remapping_dict[a] for a in lro_attribs]
        print("Our columns will be {}".format(columns))
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for r in dict_of_readers.values():
            writer.writerow({"Reader ID": r.id,
                            "Title": r.title,
                            "Author": r.author,
                            "Type-Token Ratio": r.tt_ratio,
                            "Type Ct": r.type_ct,
                            "Token Ct": r.token_ct,
                            "Unique Words": r.unique_words,
                            "Word Ct": r.word_ct,
                            "Page Ct": r.page_ct,
                            "Avg Length of Words (# Chars)": r.word_len_char,
                            "Avg Length of Sentences (# Words)": r.sent_len_word,
                            "Words w Counts": r.words,
                            "Content": r.content})
    print("Results of your analyses have been written to \n\t" +
          "{}\nPlease review.".format(full_path))
    # except:
    #     print("Sorry, that directory and filename will not work. Let's try again.")
    #     output_to_file(dict_of_readers)
    # except:
        # exit_ttr()


#########################
# Top-Level Interaction #
#########################
proceed = True
while proceed:
    running_mode, verbosity = user_interaction()
    file_list = get_dir_and_file(running_mode)
    for f in file_list:
        process_reader(f, verbosity)
    # if running_mode == "m":
    #     file_list = get_dir_and_file(running_mode)
    proceed = processing_complete(running_mode)
        # process_reader(f, verbosity)