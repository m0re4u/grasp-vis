from KafNafParserPy import KafNafParser


def load_naf(filename):
    naf_parser = KafNafParser(filename)
    return naf_parser