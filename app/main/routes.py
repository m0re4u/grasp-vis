from app.main import bp
import app.utils.data_loader as dl

from flask import (render_template, request, jsonify, current_app, Markup)


def add_event_spans_to_text(text):
    """
    Add span elements to the raw text, to highlight all the found events.
    """
    SPAN_TEMPLATE = "<span id={eid}>{event_text}</span>"
    new_text = text
    # Go backwards through list, starting at the end of the text to preserve character offset
    sorted_events = {k:v for k,v in sorted(current_app.fact_dict.items(), key=lambda item: item[1]['offset'], reverse=True)}
    for event_id, ed in sorted_events.items():
        event_text = text[ed['offset']:ed['offset']+ed['length']]
        assert event_text == " ".join(ed['words'])
        new_text = text[:ed['offset']] + SPAN_TEMPLATE.format(eid=event_id, event_text=event_text) + new_text[ed['offset']+ed['length']:]

    return Markup(new_text)


@bp.route('/')
@bp.route('/index')
def hello():
    txt = current_app.parsed_naf.get_raw()
    new_txt = add_event_spans_to_text(txt)
    events = [(k, " ".join(x['words'])) for k, x in current_app.fact_dict.items()]
    return render_template('index.html', text=new_txt, events=events)