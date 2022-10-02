from convokit import Corpus, download


corpus = Corpus(filename=download("iq2-corpus"))


print(corpus.print_summary_stats())