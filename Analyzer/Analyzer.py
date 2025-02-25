# - Import Necessary Headers
from Configs import *

# - Analyzer Class Definition
class Analyzer:
    # - Constructor
    def __init__(self, papers):
        # - Papers
        self.papers = papers
        # - Show Howmany Papers are Loaded into Analyzer
        printRKPA(ANALYZER, SUCCESS, f"Loaded {INFO}{len(self.papers)}{RESET} Papers")
        # - Set Keyword Synonyms
        self.keyword_synonyms = KEYWORD_SYNONYMS
        # - Top Keywords
        self.top_keywords = []
    # - Method to Analyze Journals
    def journals(self):
        # - Create a List of Journals
        journal_list = [paper.get('journal', 'Unknown') for paper in self.papers if paper.get('journal')]
        # - Count the Journals
        journal_counts = Counter(journal_list)
        # - Get Top N Most Common Journals
        top_journals = journal_counts.most_common(TOP_N_JOURNALS)
        # - Separate Labels and Counts 
        journals, counts = zip(*top_journals)
        # - Plot the Data
        plt.figure(figsize = (12, 10))
        bars = plt.barh(journals, counts, color = '#888DA7')
        plt.xlabel("Number of Papers", fontsize = 14)
        plt.ylabel("Journals", fontsize = 14)
        plt.title(f"Top {TOP_N_JOURNALS} Journals by Number of Papers", fontsize = 16)
        plt.gca().invert_yaxis()
        plt.xticks(fontsize = 12)
        plt.yticks(fontsize = 10)
        # - Annotate the Bars
        for bar, count in zip(bars, counts):
            plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, str(count), va='center', fontsize=12)
        # - Save the Plot
        plt.savefig(
            DATA_DIR + JOURNALS_PLOT,
            bbox_inches = "tight"
        )
        plt.close()
        # - Show Success Message
        printRKPA(ANALYZER, SUCCESS, "Journals Analysis Completed")
    # - Method to Analyze Publishers
    def publishers(self):
        # - Create a List of Publishers
        publisher_list = [paper.get('publisher', 'Unknown') for paper in self.papers if paper.get('publisher')]
        # - Count the Publishers
        publisher_counts = Counter(publisher_list)
        # - Get Top N Most Common Publishers
        top_publishers = publisher_counts.most_common(TOP_N_PUBLISHERS)
        # - Separate Labels and Counts
        publishers, counts = zip(*top_publishers)
        # - Plot the Data
        plt.figure(figsize = (12, 10))
        bars = plt.barh(publishers, counts, color = '#888DA7')
        plt.xlabel("Number of Papers", fontsize = 14)
        plt.ylabel("Publishers", fontsize = 14)
        plt.title(f"Top {TOP_N_PUBLISHERS} Publishers by Number of Papers", fontsize = 16)
        plt.gca().invert_yaxis()
        plt.xticks(fontsize = 12)
        plt.yticks(fontsize = 10)
        # - Annotate the Bars
        for bar, count in zip(bars, counts):
            plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, str(count), va='center', fontsize=12)
        # - Save the Plot
        plt.savefig(
            DATA_DIR + PUBLISHERS_PLOT,
            bbox_inches = "tight"
        )
        plt.close()
        # - Show Success Message
        printRKPA(ANALYZER, SUCCESS, "Publishers Analysis Completed")
    # - Method to Analyze Keywords
    def keywords(self):
        # - Create a List of Keywords
        keyword_list = []
        # - Iterate Over Papers
        for paper in self.papers:
            keywords = paper.get('keywords', '')
            # - Separate Keywords
            for keyword in keywords.split(','):
                keyword = keyword.strip().lower()
                keyword = self.replace_synonyms(keyword)
                keyword_list.append(keyword)
        # - Count the Keywords
        keyword_counts = Counter(keyword_list)
        # - Get Top N Most Common Keywords
        self.top_keywords = keyword_counts.most_common(TOP_N_KEYWORDS)
        # - Separate Labels and Counts 
        keywords, counts = zip(*self.top_keywords)
        # - Plot the Data
        plt.figure(figsize = (12, 10))
        plt.title(f"Top {TOP_N_KEYWORDS} Keywords by Frequency", fontsize = 16)
        bars = plt.barh(keywords, counts, color = '#888DA7')
        plt.xlabel("Number of Occurrences", fontsize = 14)
        plt.ylabel("Keywords", fontsize = 14)
        plt.gca().invert_yaxis()
        plt.xticks(fontsize = 12)
        plt.yticks(fontsize = 10)
        # - Annotate the Bars
        for bar, count in zip(bars, counts):
            plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, str(count), va = 'center', fontsize=12)
        # - Save the Plot
        plt.savefig(
            DATA_DIR + KEYWORDS_PLOT,
            bbox_inches = "tight"
        )
        plt.close()
        # - Show Success Message
        printRKPA(ANALYZER, SUCCESS, "Keywords Analysis Completed")
    # - Method to Replace Synonyms with Canonical Keywords
    def replace_synonyms(self, keyword):
        for canonical, synonyms in self.keyword_synonyms.items():
            if keyword in [synonym.lower() for synonym in synonyms]:
                return canonical
        return keyword
    # - Method to Analyze Specific Keywords
    def specificKeywords(self):
        # - Extract the First Configured Keywords and Their Total Occurrences
        keyword_totals = {k[0]: k[1] for k in self.top_keywords[:TOP_N_KEYWORDS_PER_YEAR]}
        keywords = list(keyword_totals.keys())
        # - Initialize Dictionaries to Store Keyword Counts and Top Synonyms
        year_keyword_counts = defaultdict(lambda: defaultdict(int))
        year_top_synonyms = defaultdict(lambda: defaultdict(list))
        # - Count Occurrences of each Keyword Per Year, Considering Synonyms
        for paper in self.papers:
            year = paper["year"]
            if 2009 <= int(year) <= 2025:
                paper_keywords = paper["keywords"].lower().split(", ")
                for keyword in keywords:
                    synonyms = KEYWORD_SYNONYMS.get(keyword, []) + [keyword.lower()]
                    matched_synonym = None
                    for syn in synonyms:
                        if syn in paper_keywords:
                            year_keyword_counts[year][keyword] += 1
                            matched_synonym = syn
                    # - Store the Top 3 Synonyms for each Keyword
                    if matched_synonym:
                        top_synonyms = year_top_synonyms[year][keyword]
                        if len(top_synonyms) < 3:
                            top_synonyms.append((matched_synonym, year_keyword_counts[year][keyword]))
                        else:
                            # - Replace the Least Frequent Synonym with the Current Synonym
                            top_synonyms.append((matched_synonym, year_keyword_counts[year][keyword]))
                            top_synonyms = sorted(top_synonyms, key = lambda x: x[1], reverse = True)[:3]
                        year_top_synonyms[year][keyword] = top_synonyms
        # - Normalize the Counts by the Total Occurrences of each Keyword
        for keyword in keywords:
            total_count = keyword_totals[keyword]
            total_found = sum(year_keyword_counts[year][keyword] for year in year_keyword_counts)
            if total_found > 0:
                scale_factor = total_count / total_found
            else:
                scale_factor = 0
            for year in year_keyword_counts:
                year_keyword_counts[year][keyword] *= scale_factor
        # - Plot the Occurrences of each Keyword Over the Years
        for keyword in keywords:
            years = [str(year) for year in range(2009, 2026)]
            occurrences = [year_keyword_counts[year].get(keyword, 0) for year in years]
            plt.figure(figsize = (14, 6))
            bars = plt.bar(years, occurrences, color = '#88BDB7')
            plt.xlabel("Year")
            plt.ylabel("Occurrences")
            plt.ylim(0, 300)
            plt.title(f"Occurrences of '{keyword}' Over the Years")
            plt.xticks(rotation = 45)
            plt.yticks(range(0, 301, 40))
            plt.grid(axis = 'y', linestyle = '--', alpha = 0.7)
            # - Annotate the Bars
            for bar, year in zip(bars, years):
                height = bar.get_height()
                if height > 0:
                    top_synonyms = year_top_synonyms[year].get(keyword, [])
                    # - Display the Occurrence
                    if top_synonyms:
                        plt.text(bar.get_x() + bar.get_width()/2, height + 3, f'{int(height)}', ha='center', va='bottom', fontsize=10)
                    # - Display the Most Frequent Synonym
                    if len(top_synonyms) > 0 and len(top_synonyms) <= 1:
                        plt.text(bar.get_x() + bar.get_width()/2, height + 15, f' ➤ {top_synonyms[0][0][:50]} (most)', ha='center', va='bottom', fontsize=7, rotation=90, color="#0033FF")
                    # - Display the First and Second Most Frequent Synonym
                    if len(top_synonyms) > 1 and len(top_synonyms) <= 2:
                        plt.text(bar.get_x() + bar.get_width()/2 - 0.1, height + 15, f' ➤ {top_synonyms[0][0][:50]} (most)', ha='center', va='bottom', fontsize=7, rotation=90, color="#0033FF")
                        plt.text(bar.get_x() + bar.get_width()/2 + 0.1, height + 15, f' ➤➤ {top_synonyms[1][0][:50]} (2nd)', ha='center', va='bottom', fontsize=7, rotation=90, color="#0033AA")
                    # - Display the First, Second and Third Most Frequent Synonym
                    if len(top_synonyms) > 2:
                        plt.text(bar.get_x() + bar.get_width()/2 - 0.2, height + 15, f' ➤ {top_synonyms[0][0][:30]} (most)', ha='center', va='bottom', fontsize=7, rotation=90, color="#0033FF")
                        plt.text(bar.get_x() + bar.get_width()/2, height + 15, f' ➤➤ {top_synonyms[1][0][:50]} (2nd)', ha='center', va='bottom', fontsize=7, rotation=90, color="#0033AA")
                        plt.text(bar.get_x() + bar.get_width()/2 + 0.2, height + 15, f' ➤➤➤ {top_synonyms[2][0][:50]} (3rd)', ha='center', va='bottom', fontsize=7, rotation=90, color="#003377")
            # - Save the Plot
            plt.savefig(
                DATA_DIR + TRENDING_KEYWORDS + f"{keyword}_trend.png",
                bbox_inches = 'tight',
                dpi = 200
            )
            plt.close()