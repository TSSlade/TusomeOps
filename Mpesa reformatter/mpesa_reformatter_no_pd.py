# Author: Timothy S. Slade
# Date: 2018-05-23
# Purpose: Efficiently reshaping and stacking Mpesa's bulk payment .CSVs
# for easy reconciliation by the Finance dept.

#---------------------
# Packages to import -
#---------------------
import csv
import os
import re
import sys
import datetime as dt
from dateutil.parser import parse
from itertools import islice
#------------------------
# High-level pseudocode -
#------------------------
# 1) Prompt user for directory from which the batch of .CSVs will be read
# 2) Loop over all .CSV files in that directory
# 3) Verify structure matches that of Mpesa Bulk Payment Report (MBPR)
#    If yes, continue. If no, move to next file.
# 4) Process file per detailed pseudocode
# 5) Generate .CSV of consolidated MBPRs
# 6) Prompt user for Master file onto which consolidated MBPR data will
#    be appended
# 7) Load -Master- file
# 8) Append consolidated MBPRs
# 9) Save -Master- file

#--------------------
# Custom Exceptions -
#--------------------

class FileOutofRangeError(Exception):
    """ Exception raised when the user provided an entry at the file list 
        verification stage which was out of range
    """
    #print("That is not a valid entry - it cannot be found within the list. " +
    #    "Please provide another entry.")


#--------------------
# Classes / Objects -
#--------------------
sending_routine_dict = {
    "verify": ["[C] for 'confirm' (that all files listed are to be analyzed)",
               "[R] for 'remove' (to remove a file from the list provided)"],
    "output_fname": ["[A] to 'accept' the default filename",
                     "[C] to 'choose' a different filename"],
    "output_dname": ["[A] to 'accept' the current output directory",
                     "[C] to 'choose' a different output directory"],
    "file_selector": ["[#]: numerals matching an entry in the list of files " +
                      "to process"]
}
stage_dict = {
    "processing": ["Please provide the directory in which your files are stored",
                   "",
                   "The following files will be processed:"],
    "consolidating": ["Please provide the directory in which your Master " +
                      "file is located.",
                      "MBPR",
                      "The following files will be appended to your Master " +
                      "file:"]
}

session_dict = {}

#------------
# Functions -
#------------

def exit_mbpc():
    """ Function to gracefully leave MpesaBulkPaymentConsolidator """
    print("Thank you for using Mpesa Bulk Payment Report Consolidator. Good-bye.")
    sys.exit(1)


def get_dir_and_file(stage):
    """ Function to get input from the user. Input includes the stage of the
        process the loop is in: [processing] of MPBRs or [consolidating] of
        processed MBPRs
    """
    ask, suffix, feedback = stage_dict[stage][0:3]
    print("-" * 126)
    print()
    print(ask)
    active_dir = input("\t >>: ")
    print()
    exit_mbpc() if active_dir == "q" else active_dir
    backslash = re.compile(r"\\")
    try:
        active_dir = re.sub(backslash, "/", active_dir)
        os.chdir(active_dir)
        if stage == "processing":
            file_list = [f for f in
                     os.listdir(active_dir) if
                     os.path.isfile(os.path.join(active_dir, f)) and
                     f.endswith(f"{suffix}.csv")]
        elif stage == "consolidating":
            file_list = [f for f in session_dict]
    except OSError:
        print(f"Your entry [{active_dir}] wasn't recognized as a valid " +
                "directory. Please try again!")
        get_dir_and_file(stage)

    print("-" * 126)
    print()
    print(feedback)
    confirmation, file_list = verify_file_list(file_list)
    print()
    if stage=="consolidating":
        print("Please provide the name of the .csv file to which these files " +
            "should be appended. (No file extension needed.)")
        #target_file = input("\t >>: ") + ".csv"
        target_file = active_dir + input("\t >>: ") + ".csv"
    elif stage=="processing":
        target_file = None
    exit_mbpc() if confirmation == "q" else confirmation
    if confirmation == "c":
        print("Thank you. We'll proceed. \n")
    return file_list, target_file


def verify_file_list(file_list):
    """ Function to nicely print out the current file list through which
        the -process_mbpr- function will loop.
    """
    print()
    print("~" * 126)
    print_file_list(file_list)
    print("Please [C]onfirm the list is accurate. If there are any files you " +
            "want to [R]emove from the list, now is the time.")
    confirmation = input("\t >>: ").lower()
    print()
    while confirmation not in "rcq":
        confirmation = input_nudge("verify")
        print()
    if confirmation == "r":
        file_to_drop = ""
        while file_to_drop is not "f":
            print("-" * 126)
            print()
            print("Please provide the number for the file you wish to remove.\n" +
                  "When you have [F]inished, please enter 'F'.")
            file_to_drop = str(input("\t >>: ")).lower()
            print()
            if file_to_drop == "f":
                confirmation = "c"
                break
            elif re.match("[0-9]+", file_to_drop):
                try:
                    removed = file_list.pop(int(file_to_drop) - 1)
                    print(f"{removed} removed.\n")
                except IndexError:
                    raise(FileOutofRangeError)
                    print(f"Words")
                    #        "provide another entry.")
                print_file_list(file_list)
            elif file_to_drop == "q":
                exit_mbpc()
            else:
                input_nudge("file_selector")
        if file_to_drop == "f":
            confirmation = "c"
    elif confirmation == "q":
        exit_mbpc()
    return confirmation, file_list
    #return file_list


def print_file_list(file_list):
    """ Function to nicely print out the current file list through which
        the -process_reader- function will loop.
    """
    file_num = 0
    for f in file_list:
        file_num += 1
        print(f"[{file_num:>2}]\t{f}")
    print("~" * 126)
    print()


def input_nudge(sending_routine):
    """ Routine to remind the user of their input options.
    """
    print("." * 126)
    print("Sorry, that input was not understood. To recap, valid inputs are")
    valid_responses = sending_routine_dict[sending_routine]
    for option in valid_responses:
        print(f"\t{option}\n")
    print("." * 126)
    print("\t[q] for 'quit' (to quit the Mpesa Bulk Payment Report " +
        "Consolidator without writing the results to file)")
    new_command = input("\t >>: ").lower()
    exit_mbpc() if new_command == "q" else new_command
    return new_command


def user_interaction(stage):
    """ Function to govern user interaction, including obtaining the
        preferred -running_mode- and -verbosity-, and calling the
        -get_dir_and_file- function
    """
    print("-" * 126)
    print()
    mbpr_list, target_file = get_dir_and_file(stage)
    print("-" * 126)
    print()
    #verify_file_list(mbpr_list)
    print()
    print("List verified...")
    return mbpr_list, target_file

def convert(datestr):
    converted = dt.datetime.strptime(str(datestr), "%d%m%Y %H:%M:%S")
    return converted

def process_mbpr(file_to_process):
    """ Function to import Mpesa Bulk Payment Report .CSV, re-order the
        columns, and store in a dataframe for later stacking.
    """
    # with open(full_path, "w", newline="") as csvfile:
    varnames = ["record_num", "val_result", "year",
                "month", "day", "time", "trans_det", "trans_id", "amt_sent",
                "fee_1", "fee_2", "status", "err_code", "err_msg"]
    bulk_plan_dets = []
    record_num = []
    val_result = []
    year = []
    month = []
    day = []
    time = []
    trans_det = []
    trans_id = []
    amt_sent = []
    fee_1 = []
    fee_2 = []
    status = []
    err_code = []
    err_msg = []

    with open(file_to_process, newline="", mode="r") as csvfile:
        bulkreport = csv.reader(csvfile)
        row_ct = 0
        for row in bulkreport:
            row_ct += 1
            if len(row) > 0:
                if row[0] == "Organization Name":
                    bulk_plan_dets_row = row_ct + 1
                    print(f"The bulk plan details are in row {row_ct}") 
                elif row[0] == "Record No":
                    content_start_row = row_ct + 1  
                    print(f"Content will begin in row {row_ct}")
                #else:
            else:
                continue

        print("Finished first loop through column 0")
        print(f"Bulk plan details are in row {bulk_plan_dets_row}")
        print(f"Content begins from row {content_start_row}")

    with open(file_to_process, newline="", mode="r") as csvfile:
        bulkreport = csv.reader(csvfile)
        row_ct = 0
        record_ct = 0
        for row in bulkreport:
            row_ct += 1
            if len(row) > 0: 
                if row_ct == bulk_plan_dets_row:
                    bulk_plan_dets.append(row[1])
                    bulk_plan_dets.append(row[2])
                    print(bulk_plan_dets)
                elif row_ct >= content_start_row:
                    record_ct += 1
                    #print(f"We are currently on row {row_ct}, record {record_ct}")
                    #print(row)
                    record_num.append(row[0])
                    val_result.append(row[1])
                    year.append(row[2][4:8])
                    month.append(row[2][0:2])
                    day.append(row[2][2:4])
                    time.append(row[2][10:])
                    #finished_time.append(row[3])
                    trans_det.append(row[5])
                    trans_id.append(row[4])
                    amt_sent.append(row[6])
                    fee_1.append(row[7])
                    fee_2.append(row[8])
                    status.append(row[9])
                    err_code.append(row[10])
                    try:
                        err_msg.append(row[11])
                    except:
                        err_msg.append("")
                        continue
            else:
                continue

    print(f"There were {row_ct - 1} rows containing {record_ct} records in this document")

    filename = year[0] + month[0] + day[0] + "-" + trans_id[record_ct - 1] + "-MBPR.csv"  

    with open(filename, newline="", mode="w") as csvfile:
        processed = csv.writer(csvfile)
        processed.writerow([bulk_plan_dets[0], bulk_plan_dets[1]])
        processed.writerow([varnames, "bulk_plan_dets"])
        i = 0
        while i < record_ct:
            processed.writerow([record_num[i],
                                val_result[i],
                                year[i],
                                month[i],
                                day[i],
                                time[i],
                                trans_det[i],
                                trans_id[i],
                                amt_sent[i],
                                fee_1[i],
                                fee_2[i],
                                status[i],
                                err_code[i],
                                err_msg[i],
                                bulk_plan_dets[0],
                                bulk_plan_dets[1]])
            i += 1
    processing_complete(filename)
    file_contents = [bulk_plan_dets, record_num, val_result,
                     year, month, day, time, trans_det,
                     trans_id, amt_sent, fee_1, fee_2,
                     status, err_code, err_msg]
    session_dict[filename] = file_contents
    return file_contents

def stack_mbpr(dict_of_files, target_file):
    """ Function to import Mpesa Bulk Payment Report .CSV, re-order the
        columns, and store in a dataframe for later stacking.
    """
    print(f"In the stacker, targeting: {target_file}")
    counter = 0
    for mbpr in session_dict:
        with open(target_file, 'a', newline="") as new_file, open(mbpr, 'r') as main_file:
            target = csv.writer(new_file)
            source = csv.reader(islice(main_file, 2, None))
            if counter == 0:
                target.writerow(["record_num", "val_result",
                                 "year", "month", "day",
                                 "time", "trans_det", "trans_id", "amt_sent",
                                 "fee_1", "fee_2", "status", "err_code",
                                 "err_msg", "bulk_plan_dets"])
            elif counter > 0:
                next(source, None)
            for row in source:
                target.writerow(row)
        counter += 1


def processing_complete(filename):
    """ Routine to run when file processing has completed.
    """
    print("Restructuring of the following MBPR has been completed: ")
    #print_file_list(filename)
    print(f"\t{filename}")
    print()
    proceed = True
    return proceed

#---------------
# Control Loop -
#---------------
proceed = True
while proceed:
    to_process = user_interaction("processing")[0]
    for mbpr in to_process:
        print(f"Processing {mbpr}...")
        process_mbpr(mbpr)
    print(f"The following files have been reformatted:")
    print_file_list(session_dict.keys())
    to_stack, target = user_interaction("consolidating")
    stack_mbpr(to_stack, target)


# 1) load the csv
# 2) check whether the header in row 1 matches the expected header for a bulk payment file
# 3) store the bulk plan name and description
# 4) load data beginning from row 13 (headers)
# 5) re-order columns as follows:
# 1: receipt_no
# 2: transaction_id <- chars4:6 of column TransactionID (discard the leading 4 and trailing 3 digits)
# 3: date in yy/mm/dd format <-- extracted from Finished Timestamp column
# 4: details <- Transaction Details column (recipient # and name)
# 5: transaction_status <- Status
# 6: withdrawn <- Amount
# 7: fee <- sum(Fee Charge)
# 8: extra_fee <- Extra Fee Charge
# 6) Records being imported is conditional on transaction_status=="Completed"
# 7) a master dataset is created from CSV #1
# 8) subsequent CSVs are stacked below it
# 9) once all CSVs exhausted, master dataset is exported to a single consolidated CSV
# 10) filename of exported CSV will be Consolidated Mpesa Bulk Payment YYYYMMDD
# 9: extra column: contains Bulk Plan Name - Bulk Plan Description
# 