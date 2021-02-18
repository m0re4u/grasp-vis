def get_pred_type(p):
    PRED_TYPES = ['default', 'lexical']
    if 'denotedBy' in str(p):
        pred_type = 'lexical'
    else:
        pred_type = 'default'

    assert pred_type in PRED_TYPES
    return pred_type