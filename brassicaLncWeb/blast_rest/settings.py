"""
user defined blast app settings file
"""

import os

BASE_DIR = os.path.dirname(__file__)

SAMPLE_DIR = os.path.join(BASE_DIR, 'data/')

BLAST_DB_NUCL_LIST = [
    {
        "name": "lnc",
        "path": 'data/db/lnc_db',
        "desc": "brancica lnc",
        "annotated": False, },
]



BLAST_DB_NUCL_CHOICE = [(os.path.join(BASE_DIR, db["path"]), db["desc"]) for db in BLAST_DB_NUCL_LIST]



# maximum number of query sequences in from
BLAST_MAX_NUMBER_SEQ_IN_INPUT = 10



# scoring Matrix sets
MATRIX_LIST = ['BLOSUM45', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM30', 'PAM70']
MATRIX_CHOICE_LIST = list((x, x,) for x in MATRIX_LIST)
MATRIX_DEFAULT = 'BLOSUM62'

# e-value sets
EVALUE_LIST = [1, 0.001, 1e-5, 1e-6, 1e-10, 1e-30, 1e-50, 1e-100]
EVALUE_CHOICE_LIST = list((x, str(x),) for x in list(EVALUE_LIST))
EVALUE_BLAST_DEFAULT = 0.001

# parameters for sensitive nucleotide search
NUCLEOTIDE_SEARCH_SENSITIVE_CHOICE = (("{'gapopen': 5, 'gapextend': 2, 'penalty': -3, 'reward': 2}", "NORMAL",),
                                      ("{'penalty': -3, 'word_size': 15,'gapopen': 5, 'gapextend': 2,  'reward': 1, }",
                                       "NEAR MATCH",),
                                      ("{'penalty': -1, 'word_size': 9,'gapopen': 2, 'gapextend': 1,  'reward': 1, }",
                                       "DISTANT",),)



class BlastLimitSet(object):
    def __init__(self, default_word_size, min_word_size, max_word_size):
        self.default_word_size = default_word_size
        self.min_word_size = min_word_size
        self.max_word_size = max_word_size

    def get_word_size_error(self):
        return "word size should be between {} and {}".format(self.min_word_size, self.max_word_size - 1)


BLASTN_SETS = BlastLimitSet(default_word_size=11, min_word_size=7, max_word_size=50)

# ERROR massages
BLAST_CORRECT_SEQ_ERROR_MSG = "Please put correct sequence!"
BLAST_CORRECT_SEQ_MAX_SEQ_NUMB_ERROR_MSG = "Too many sequences, maximum is {}".format(BLAST_MAX_NUMBER_SEQ_IN_INPUT)
BLAST_CORRECT_SEQ_TOO_SHORT_ERROR_MSG = "Too short sequence!"
BLAST_CORRECT_PARAMS = "Sorry, incorrect parameter combination"
