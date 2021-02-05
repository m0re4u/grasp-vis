from grasp_app.main import bp
import grasp_app.utils.data_loader as dl

from flask import (render_template, request, jsonify, current_app, Markup, redirect, url_for, flash)

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
    return jsonify(fact_info=current_app.fact_dict[event_id]['words'], fact_values=factvalues, srl=current_app.fact_dict[event_id]['srl']['roles'])


@bp.route('/file_view',  methods=['GET', 'POST'])
def show_file():
    # Redirect back to file selector page if no file is requested
    if 'file_selector' not in request.form:
        flash("You did not specify a file to load!", 'warning')
        return redirect('index')
    filename = request.form['file_selector']

    # Load file
    current_app.parsed_naf = dl.load_naf(filename)
    text = Markup(" ".join([f"<span id=\"{token.get_id()}\">{token.get_text()}</span>" for token in current_app.parsed_naf.get_tokens()]))

    current_app.fact_dict = dl.get_all_factualities(current_app.parsed_naf)

    # Sort events based on their occurrence in the text, from back to front
    sorted_events = {k:v for k,v in sorted(current_app.fact_dict.items(), key=lambda item: item[1]['offset'], reverse=False)}
    events = [(k, " ".join(sorted_events[k]['words']), "-".join(sorted_events[k]['word_ids'])) for k in sorted_events]
    return render_template('file_view.html', text=text, events=events)

@bp.route('/')
@bp.route('/index')
def hello():
    files = [
        'data/test.ec.final.naf',
        'data/heidag.ec.final.naf'
        ]
    return render_template('index.html', files=files)