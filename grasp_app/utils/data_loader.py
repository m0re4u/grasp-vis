import rdflib
from KafNafParserPy import KafNafParser
from flask import Markup, current_app

def load_naf(filename):
    """
    Load a NAF file.
    """
    naf_parser = KafNafParser(filename)
    return naf_parser


def load_trig(filename):
    g = rdflib.Graph()
    g.parse(filename)
    return g


def get_srl_dict(parsed_naf):
    """
    Extract srl predicates and their roles, lexically anchored to the original
    text.
    """
    # Extract SRL predicates + roles
    srl_predicates = {}
    for predicate in parsed_naf.get_predicates():
        predicate_span = "".join([y.get_id() for y in predicate.get_span()])
        roles = {}
        for role in predicate.get_roles():
            semrole = role.get_semRole()
            spans = []
            for span in role.get_span():
                wf_ids = []
                for wf in parsed_naf.term_layer.get_term(span.get_id()).get_span_ids():
                    wf_id = parsed_naf.text_layer.get_wf(wf).get_id()
                    if wf_id is None:
                        wf_id=""
                    wf_ids.append(wf_id)
                spans.extend(wf_ids)

            roles[semrole] = spans

        value = {
            'id': predicate.get_id(),
            'roles': roles
            }

        srl_predicates[predicate_span] = value
    return srl_predicates

def get_all_factualities(parsed_naf):
    """
    Get a dict with the following:

    Events and their factuality, consisting of its
     - id
     - words it is denoted by
     - the lowest of the character offsets for all words
     - the total length of all words

    Accompanying every event is an semantic role labeling overview, showing the
    recognized roles (and the text it is denoted by).
    """

    # Extract factualities
    fact_dict = {}
    for fact in parsed_naf.get_factualities():
        fact_id = fact.get_id()
        fact_dict[fact_id] = {
            'word_ids': [],
            'words': [],
            'offset': [],
            'length': []
        }
        for target in fact.get_span():
            wfs = parsed_naf.term_layer.get_term(target.get_id()).get_span_ids()
            for wf in wfs:
                _wf = parsed_naf.text_layer.get_wf(wf)
                fact_dict[fact_id]['word_ids'].append(_wf.get_id())
                fact_dict[fact_id]['words'].append(_wf.get_text())
                fact_dict[fact_id]['offset'].append(int(_wf.get_offset()))
                fact_dict[fact_id]['length'].append(int(_wf.get_length()))
        # Take lowest offset
        fact_dict[fact_id]['offset'] = min(fact_dict[fact_id]['offset'])
        # Sum all lengths
        fact_dict[fact_id]['length'] = sum(fact_dict[fact_id]['length'])

        # Add SRL
        srl_dict = get_srl_dict(parsed_naf)
        tgts = "".join([x.get_id() for x in fact.get_span()])
        if tgts in srl_dict:
            fact_dict[fact_id]['srl'] = srl_dict[tgts]
        else:
            # Delete facts where an SRL predicate or role has no span
            del fact_dict[fact_id]

    return fact_dict