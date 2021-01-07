from app.main import bp
import app.utils.data_loader as dl

from flask import render_template, request, jsonify, current_app


@bp.route('/highlight_event', methods=['POST', 'GET'])
def highlight_event():
    print("test")
    event_id = request.args.get('event_id')
    return jsonify(offset=current_app.fact_dict[event_id]['offset'], length=current_app.fact_dict[event_id]['length'])


@bp.route('/')
@bp.route('/index')
def hello():
    txt = current_app.parsed_naf.get_raw()
    events = [(k, " ".join(x['words'])) for k, x in current_app.fact_dict.items()]
    return render_template('index.html', text=txt, events=events)