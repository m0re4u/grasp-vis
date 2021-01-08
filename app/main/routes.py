from app.main import bp
import app.utils.data_loader as dl

from flask import (render_template, request, jsonify, current_app, Markup)

@bp.route('/select_event', methods=['GET', 'POST'])
def select_event():
    """
    Get the factuality values for a given event

    TODO: replace loop with a (atm nonexistent) "get" by id.
    """
    event_id = request.args.get('event_id')
    factvalues = []
    for fact in current_app.parsed_naf.factuality_layer.get_factualities():
        if fact.get_id() == event_id:
            values = fact.get_factVals()
            for value in values:
                factvalues.append((value.get_resource(), value.get_value()))
    return jsonify(result=factvalues)


def add_event_spans_to_text(text, sorted_events):
    """
    Add span elements to the raw text, to highlight all the found events.
    """
    SPAN_TEMPLATE = "<span id={eid}>{event_text}</span>"
    new_text = text
    for event_id, ed in sorted_events.items():
        event_text = text[ed['offset']:ed['offset']+ed['length']]
        assert event_text == " ".join(ed['words'])
        new_text = text[:ed['offset']] + SPAN_TEMPLATE.format(eid=event_id, event_text=event_text) + new_text[ed['offset']+ed['length']:]

    return Markup(new_text)


@bp.route('/')
@bp.route('/index')
def hello():
    txt = current_app.parsed_naf.get_raw()
    # Sort events based on their occurrence in the text, from back to front
    sorted_events = {k:v for k,v in sorted(current_app.fact_dict.items(), key=lambda item: item[1]['offset'], reverse=True)}
    new_txt = add_event_spans_to_text(txt, sorted_events)

    reversed_se = list(reversed(list(sorted_events.keys())))
    events = [(k, " ".join(sorted_events[k]['words'])) for k in reversed_se]
    return render_template('index.html', text=new_txt, events=events)