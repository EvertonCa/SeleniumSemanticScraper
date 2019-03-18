# SeleniumSemanticScraper
Automatically crawl meta data from papers from Semantic Scholar, based on a given key phrase using Selenium WebDriver and saves it in a .xls (Excel) file.

# Running
This program can run in **Windows, Linux and MacOS**.
- Install the latest version of **Python 3** in your system.
- Make sure you have the following packages installed: **Selenium, xlsxwriter, pickle and pathlib**. This can be done with PIP or any other Python packages manager.
- Make sure you have **Google Chrome** installed (the program will open a headless version of Chrome and make the search on it)
- Run the file **SemanticScholarMetaCrawler.py** with the command `python SemanticScholarMetaCrawler.py` on your terminal or cmd.

The first question will ask you to put your desired search. This is the same phrase you would put in the semanticscholar.org site.

The second question wants to know how many pages do you like to be scrapped. Note that each page will mean that the program will search for one page without any filter, then another page with the Last Five Years filter active and another page with the Lit Reviews filter active. In another words, each page will mean that the program will search for 3 pages with different filters. Around 30 results for page.

A message with each article successfully searched will be displayed in the terminal. After the search is complete, a .xls file will be generated in the folder **/Files/YOUR SEARCH/**.

# Multiple Searches
When searching for multiple subjects, you can use the file **UniteArticles.py** to generate one Excel file for all the searches you've made.
Run the file by the command `python UniteArticles.py` and copy all the **.pkl** files from your previous searches to the folder **Unite**.
Rename the files so that they have a increasing number sequency after their names. For example:

**Articles1.pkl**

**Articles2.pkl**

**Authors1.pkl**

**Authors2.pkl**

Press ENTER. After that the Excel file will be generated in the same folder.
