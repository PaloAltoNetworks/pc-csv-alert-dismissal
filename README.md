# Overview

This script accepts a CSV file that contains Alert IDs and Dismissal Reasons.

The script groups Alerts by their Dismissal Reason and dismisses Alerts in batches.

# Installation
pip3 install loguru
pip3 install pcpi

# Running the script

Defaults to file named "input.csv".
```python3 dismiss.py```

Specify the path to the input csv using the "-file" option.
```python3 dismiss.py -file inputfilename.csv```

# Notes

### One
The script accepts a csv file with the following format:
```Alert ID,Policy Name,dismissalNote```

### Two
The script is set to read credentials from a file by default. If the file does not exist, then the script will create the file for you.

You can also have the script read from environment variables or directly from the user.

Authentication with Prisma Cloud is handled by pcpi (Prisma Cloud Python Integration).
Please refer to the GitHub page for this library for more details.
[https://github.com/PaloAltoNetworks/pc-python-integration](https://github.com/PaloAltoNetworks/pc-python-integration)
