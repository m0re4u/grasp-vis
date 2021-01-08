from KafNafParserPy import KafNafParser


def load_naf(filename):
    """
    Load a NAF file.
    """
    naf_parser = KafNafParser(filename)
    return naf_parser

def get_all_factualities(parsed_naf):
    """
    Get a dict with the following:

    For every factuality, its
     - id
     - words it is denoted by
     - the lowest of the character offsets for all words
     - the total length of all words
    """

    srl_predicates = {
        "".join([y.get_id() for y in x.get_span()]): {
            'id': x.get_id(),
            'roles': [(r.get_semRole()) for r in x.get_roles()]
            }
            for x in parsed_naf.get_predicates()
    }
    fact_dict = {}
    for fact in parsed_naf.get_factualities():
        fact_id = fact.get_id()
        fact_dict[fact_id] = {'words': [], 'offset': [], 'length': []}
        for target in fact.get_span():
            wfs = parsed_naf.term_layer.get_term(target.get_id()).get_span_ids()
            for wf in wfs:
                _wf = parsed_naf.text_layer.get_wf(wf)
                fact_dict[fact_id]['words'].append(_wf.get_text())
                fact_dict[fact_id]['offset'].append(int(_wf.get_offset()))
                fact_dict[fact_id]['length'].append(int(_wf.get_length()))
        # Take lowest offset
        fact_dict[fact_id]['offset'] = min(fact_dict[fact_id]['offset'])
        # Sum all lengths
        fact_dict[fact_id]['length'] = sum(fact_dict[fact_id]['length'])

        # Add SRL roles
        tgts = "".join([x.get_id() for x in fact.get_span()])
        fact_dict[fact_id]['srl'] = srl_predicates[tgts]

    return fact_dict