# - Import Analyzer Module
from Analyzer.Analyzer import *
# - Import Extractor Module
from Data.Extractor import *

# - Create Extractor Object
extractor = Extractor()
# - Load Data
extractor.load()
# - Convert to JSON
extractor.extract()

# - Create Analyzer Object
analyzer = Analyzer(extractor.papers)
# - Analyze Journals
analyzer.journals()
# - Analyze Publishers
analyzer.publishers()
# - Analyze Keywords
analyzer.keywords()
# - Analyze Specific Keywords
analyzer.specificKeywords()