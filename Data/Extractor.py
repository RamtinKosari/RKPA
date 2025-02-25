# - Import Necessary Headers
from Configs import *

# - Extractor Class Definition
class Extractor:
    # - Constructor
    def __init__(self):
        # - Papers
        self.papers = []
    # - Method to Load Data File
    def load(self, path = os.path.join(DATA_DIR, DATA_FILE)):
        # - Check if File Exists
        if not os.path.exists(path):
            printRKPA(EXTRACTOR, FAILED, "Data File Not Found")
            return False
        # - Open File
        with open(path, 'r', encoding = 'utf-8') as file:
            rows = csv.reader(file)
            for row in rows:
                # - Clean row, Remove Spaces and Ignore '-' or Rmpty Values
                cleaned_row = [col.strip() if col.strip() != '-' else '' for col in row]
                # - Check if the Row is Empty After Cleaning
                if any(cleaned_row):  
                    paper_dict = dict(zip(HEADERS, cleaned_row))
                    self.papers.append(paper_dict)
                printRKPA(EXTRACTOR, SUCCESS, f"Loaded Paper {INFO}{paper_dict['title'][:20]} ...{RESET}")
        # - Show Howmany Papers are Loaded
        printRKPA(EXTRACTOR, SUCCESS, f"Loaded {INFO}{len(self.papers)}{RESET} Papers")
        return True
    # - Method to Extract Data into JSON Format
    def extract(self):        
        # - Convert to JSON and Save to File
        with open(os.path.join(DATA_DIR, JSON_FILE), 'w', encoding = 'utf-8') as json_file:
            json.dump(self.papers, json_file, indent = 4)
        # - Show Success Message
        printRKPA(EXTRACTOR, SUCCESS, "Data Extracted to JSON File" + INFO + f" {JSON_FILE}")
        return True