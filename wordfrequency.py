import csv

"""
Format:

Word	FREQcount	CDcount	FREQlow	Cdlow	SUBTLWF	Lg10WF	SUBTLCD	Lg10CD
the	1501908	8388	1339811	8388	29449.18	6.1766	100.00	3.9237
to	1156570	8383	1138435	8380	22677.84	6.0632	99.94	3.9235
a	1041179	8382	976941	8380	20415.27	6.0175	99.93	3.9234
you	2134713	8381	1595028	8376	41857.12	6.3293	99.92	3.9233
and	682780	8379	515365	8374	13387.84	5.8343	99.89	3.9232
it	963712	8377	685089	8370	18896.31	5.9839	99.87	3.9231
"""

FILEPATH = "SUBTLEXus74286wordstextversion.txt"

def read_word_frequencies(filepath):
    word_frequencies = {}
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        i = 1
        for row in reader:
            if len(row) < 8:  # Ensure there are enough columns
                print(f"Skipping row with insufficient columns: {row}")
                continue
            word = row[0]
            word_frequencies[word] = {
                #'FREQcount': int(row[1]),
                #'CDcount': int(row[2]),
                #'FREQlow': int(row[3]),
                #'Cdlow': int(row[4]),
                'SUBTLWF': float(row[5]),
                #'Lg10WF': float(row[6]),
                #'SUBTLCD': float(row[7]),
                #'Lg10CD': float(row[8])
                'index': i,
            }
            i += 1
    return word_frequencies

class WordFrequency:
    def __init__(self, filepath=FILEPATH):
        self.word_frequencies = read_word_frequencies(filepath)

    def get_frequency(self, word):
        word = word.lower()
        return self.word_frequencies.get(word, {}).get('SUBTLWF', 0.0)

    def get_frequency_index(self, word):
        word = word.strip('.,!?;:"\'()[]{}<>0123456789').lower()
        if not word:
            return -1
        return self.word_frequencies.get(word, {}).get('index', -1)

    def get_all_words(self):
        return list(self.word_frequencies.keys())

if __name__ == "__main__":
    wf = WordFrequency()
    print(wf.get_frequency("the"))  # Example usage
    print(wf.get_frequency_index("the"))  # Example usage
    print(wf.get_all_words()[:10])  # Print first 10 words
    print(wf.get_frequency_index("that's"))  # Example usage
    print(wf.get_frequency_index("well"))  # Example usage