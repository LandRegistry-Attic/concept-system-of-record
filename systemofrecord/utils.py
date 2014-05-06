from collections import OrderedDict
import json

def alphabetically_sorted_dict(d):
    """
    Returns a dictionary with all keys recursively sorted alphabetically
    """
    ordered = OrderedDict()
    for k, v in sorted(d.items()):
        if isinstance(v, dict):
            ordered[k] = alphabetically_sorted_dict(v)
        else:
            ordered[k] = v
    return ordered

def canonical_json(d):
    return json.dumps(
        alphabetically_sorted_dict(d),
        separators=(',', ':')
    )
