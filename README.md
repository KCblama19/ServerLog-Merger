# ServerLogStream-Merger

**ServerLogStream-Merger** is a Python-based utility designed to automate the merging of multiple server log files into a single, chronologically ordered log file using the merge sort algorithm. It’s ideal for system administrators, developers, and anyone managing multiple server log streams.

---

## Features

- Merges multiple `.log` files from a selected input folder
- Sorts log entries based on timestamps
- Outputs a single merged `.log` file to a specified output folder
- Simple command-line interface (CLI) for easy integration

---

## How It Works

1. **Input Folder**: Contains raw `.log` files with server logs.
2. **Parsing**: Each log file is read, and timestamped lines are extracted.
3. **Merging**: A merge sort algorithm combines logs into a single, sorted list based on timestamps.
4. **Output File**: The merged logs are written into one clean `.log` file.

---

## Usage

### Requirements

- Python 3.7+
- No external dependencies required

### Run the Script

#### The program accept two running format:
1. Interactive
2. command line

#### Interactive:
- Run the program 
```bash
python log_merger.py
```
- You'll be prompted to:
- Enter the path to the folder containing your .log files (eg. ./logs)
- Enter the path where the merged file should be saved (eg. ./output)

#### Command line
- Run the program
```bash
python log_merger.py [--input_folder INPUT_FOLDER] [--output_folder OUTPUT_FOLDER]
```

## Example Folder Structure
```bash
mergeSortProject/
├── server1.log
├── server2.log
├── server3.log
├── log_merger.py
```
## Example Log File Format (Required)
Each log line should begin with a timestamp
``` bash
2023-07-17 12:00:01 Server started.
2023-07-17 12:01:45 Connection established.
```

## Output
After execution, the merged logs will be saved to the ouput folder you specify:
``` bash
MergedLog_2025-07-17_14-30-00.log
```

## Current Limitations
- Only supports logs with timestamped lines in standard YYYY-MM-DD HH:MM:SS format.

- Does not yet support:

- JSON or XML log formats

- Duplicate filtering

- Timestamp format auto-detection

- GUI mode

## Planned Features
- Add support for multiple timestamp formats

- Duplicate entry removal

- File type filtering (e.g., .log, .txt)

- GUI for easier interaction

- Real-time log merging from multiple servers

- Unit tests and CI pipeline

## Contributing
Want to contribute? Fork this repo and create a pull request! Or open an issue with suggestions or bug reports.

## License
This project is open source and free to use under the MIT License.

## Author
Abraham K.C. Blam.  
Email: abrahamblama19@gmail.com  
GitHub: @KCblama19  

## Support
If you found this project helpful, consider giving it a ⭐ on GitHub or sharing it with others!