import grasp_app.utils.data_loader as dl
import grasp_app.utils.rdf_visualizer as rv
from flask import (Markup, current_app, flash, jsonify, redirect,
                   render_template, request, url_for)
from grasp_app.main import bp


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
    file_id = request.form['file_selector']
    available_files = dl.get_available_files()
    naf_filename = available_files.iloc[int(file_id)]['NAF']
    trig_filename = available_files.iloc[int(file_id)]['TRiG']
    print(f"Loading files: {naf_filename} - {trig_filename}")

    # Load file
    current_app.parsed_naf = dl.load_naf(naf_filename)
    text = Markup(" ".join([f"<span id=\"{token.get_id()}\">{token.get_text()}</span>" for token in current_app.parsed_naf.get_tokens()]))

    current_app.fact_dict = dl.get_all_factualities(current_app.parsed_naf)

    # Sort events based on their occurrence in the text, from back to front
    sorted_events = {k:v for k,v in sorted(current_app.fact_dict.items(), key=lambda item: item[1]['offset'], reverse=False)}
    events = [(k, " ".join(sorted_events[k]['words']), "-".join(sorted_events[k]['word_ids'])) for k in sorted_events]

    # Load the parallel TRiG file for RDF visualization
    trig_data = dl.load_trig(trig_filename)
    rv.visualize(trig_data)
    return render_template('file_view.html', text=text, events=events)

@bp.route('/')
@bp.route('/index')
def hello():
    df = dl.get_available_files()
    return render_template('index.html', files=df['name'])
