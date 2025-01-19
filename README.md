# Embedded Folder Monitoring and Upload System

This project monitors a folder (`images`) for new image files, uploads them to a server, and moves uploaded files to another folder (`uploaded`).

## Requirements
- Python 3.x
- Dependencies:
  - `watchdog`: Install via `pip install watchdog`.

## How to Run
1. Clone the repository: `git clone https://github.com/u-sylvie/embedded.git`
2. Navigate to the directory: `cd embedded`
3. Install required Python libraries: `pip install -r requirements.txt`
4. Create the necessary folders (`images`, `uploaded`) if not already present.
5. Run the script: `python python.py`
6. Add new image files to the `images` folder to trigger uploads.
