import os
from datetime import datetime
import argparse

# Create an argumentParser to manage the parsing of arguments
parser = argparse.ArgumentParser(description="A command line tool that sort and merge server files")

#Define argument parser telling python to expect thes optional arguments
parser.add_argument("--input_folder", type=str, help="Path to the " \
"input folder containing the server files to process")
parser.add_argument("--output_folder",type=str, help="Path to the " \
"output folder where processed(sort and merged) files will be saved.")

#Get the command-line arguments provided by the user
args = parser.parse_args()

# Get input/output folder from args or prompt
input_path = args.input_folder or input("Enter the path to the input folder " \
"containing log files: ").strip()
output_path = args.output_folder or input("Enter the path to the output folder " \
"to save merged logs: ").strip()

# Resolve absolute paths
input_path = os.path.abspath(input_path)
output_path = os.path.abspath(output_path)

# >>>>>>>>>>>>>>>>>>>>>
# Validate input folder
# >>>>>>>>>>>>>>>>>>>>>
if not os.path.isdir(input_path):
    print(f"Error: Input folder '{input_path}' not found or invalid.")
    exit(1)

# >>>>>>>>>>>>>>>>>>>>>
# Ensure Output Folder Exists
# >>>>>>>>>>>>>>>>>>>>>  
if not os.path.exists(output_path):
    # Create the final merge folder if it doesn't exist
    print("Output folder: '{output_path}' does not exist. " \
    "Creating it...")
    os.makedirs(output_path, exist_ok=True)
        

elif not os.path.isdir(output_path):
    print(f"Error: '{output_path}' is not a valid folder.")
    exit(1)

print(f"\n Input folder: {input_path}")
print(f"Output folder: {output_path}")
print("Reading, Sorting, and merging log files...\n")

'''
The commented parts below is for DEMO Testing, it can be used to
generate fake logs files in a specify folder
for learning or debugging.

Note: You will have to manuelly provide the the log entries
which will be used to create the fake log files and write
the provided log entries to them.

Custom Data: The keys are used to create the server files.
(ie: "server1.log", "server2.log", "server3.log", etc)
logLists = {
    1: [
        "2025-07-09T10:00:00 Server1 started",
        "2025-07-09T10:05:00 Server1 connection opened"
    ],
    2: [
        "2025-07-09T10:02:00 Server2 started",
        "2025-07-09T10:07:00 Server2 received data"
    ],
    3: [
        "2025-07-09T10:01:00 Server3 booting up",
        "2025-07-09T10:06:00 Server3 running diagnostics"
    ]
}
'''
# Automatically create serverfiles base on log entries
# def create_Server_files(server_num, log_entries):
#     if not log_entries:
#         print("Empty content! The server files does have contents.")
#     else:
#         #Create the filename automatically
#         filename = f"./DSA/Array/mergeSortProject/mergelogsfiles/server{server_num}.log"
        

#         # Write the contents to the file
#         with open(filename, "w") as log_files:
#             for entries1 in log_entries:
#                 log_files.write(entries1 + "\n")

# >>>>>>>>>>>>>>>>>>>>>>>>
# Read and Parse logs data from server files
# >>>>>>>>>>>>>>>>>>>>>>>>
def readEachFile():
    #Get the folder and server files location 
    contents = os.listdir(input_path)
    log_List = []
    
    '''
    Read logs data from the server file into a log list for merging
    and sorting
    '''
    for server_files in contents:
        file_name = os.path.join(input_path, server_files)

        # Skip non log files 
        if not server_files.endswith(".log"):
            continue 

        logs = []
        with open(file_name, "r") as current_file:
            '''
            Parse the timestamp and message from the log into a list
            '''
            for line in current_file:
                text = line.strip().split()
                if not text:
                    continue
                try:
                    timestamp = datetime.fromisoformat(text[0])
                    message = " ".join(text[1:])
                    logs.append({"timestamp": timestamp, "message": message})
                except ValueError:
                    print(f"Skipping malformed line in {server_files}: {line.strip()}")

            #Store each file logs into the log list as a list 
            log_List.append(logs)
    
    #Send the log list to be sorted and merge
    return mergeMultiple(log_List)

# >>>>>>>>>>>>>>>>>>>>>>
# Merge logs data two at a time
# >>>>>>>>>>>>>>>>>>>>>>
def mergeTwo(log1, log2):
    result = []
    i = j = 0

    '''
    Sort and merge the log data from two server logs
    making sure we don't exceed the amount of logs available for
    sorting and merging.
    '''
    while i < len(log1) and j < len(log2):
        #Sort in descending order base on the timestamp of each log data
        if log1[i]["timestamp"] < log2[j]["timestamp"]:
            result.append(log1[i])
            i += 1
        else:
            result.append(log2[j])
            j += 1
    
    '''
    Make sure to check for any remaining element that 
    wasn't sorted and place them to the end of the list.
    '''
    result.extend(log1[i:])
    result.extend(log2[j:])

    # return the newly sorted and merge list of logs data
    return result

# Helper function to merge multiple files simutaneously
def mergeMultiple(log_list):
    # Make sure to merge and sort all server files log
    while len(log_list) > 1:
        merged_list = []

        #Take two server file each time and merge 
        for i in range(0, len(log_list), 2):
            log1 = log_list[i]
            if i + 1 < len(log_list):
                log2 = log_list[i + 1]
                merged = mergeTwo(log1, log2)
                merged_list.append(merged)
            else:
                merged_list.append(log1)
        
        #Store the new merge log each time till we get the final log 
        log_list = merged_list

    #Return the merge servers logs  
    writeMergeListToFile(log_list[0])
    return log_list[0]

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Write the final merge list to a new file: merge_logs.log
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def writeMergeListToFile(final_merge_list):
    '''
    Save the contents of all the server logs that was
    merge and sorted in a file to form a final merge file
    '''
    final_file = os.path.join(output_path, "final_merge_logs.log")

    with open(final_file, "w") as finalMergeFile:    
        #Extract the timestamp and message in the dict and save them as log
        for log_entry in final_merge_list:
            timestamp = log_entry["timestamp"].isoformat()
            message = log_entry["message"]
            # Converts timestamps back to ISO strings
            finalMergeFile.write(f"{timestamp} {message}\n")
    
    print("Merged logs written to {final_file}\n")

# >>>>>>>>>>>>>>>>>>>>>>>>
# Run Script
# >>>>>>>>>>>>>>>>>>>>>>>>
if __name__ == "__main__":
    sorted_List = readEachFile()
    print(sorted_List)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
----- FLAG: CODE BELOW IS FOR TESTING OR DEMO PURPOSE ONLY ------
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Custom data to work with
# logLists = {
#     1: [
#         "2025-07-09T10:00:00 Server1 started",
#         "2025-07-09T10:05:00 Server1 connection opened"
#     ],
#     2: [
#         "2025-07-09T10:02:00 Server2 started",
#         "2025-07-09T10:07:00 Server2 received data"
#     ],
#     3: [
#         "2025-07-09T10:01:00 Server3 booting up",
#         "2025-07-09T10:06:00 Server3 running diagnostics"
#     ]
# }

# '''
# Send each server file logs to a create server files for each servers
# and store them in a folder to be merge and sorted.
# '''
# for server_num, log_entries in logLists.items():
#         create_Server_files(server_num, log_entries)


# '''
# Get the server files for every servers in the server log folder
# '''
# sorted_List = readEachFile()

# # Print the sorted log data
# print(sorted_List)