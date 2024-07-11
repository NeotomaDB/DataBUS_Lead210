import DataBUS.neotomaHelpers as nh
from DataBUS import ChronControl, ChronResponse

def valid_chroncontrols(yml_dict, csv_file):
    """_Validating Chron Controls_"""
    response = ChronResponse()
    params = ['chroncontrolid', 'chronologyid', 'chroncontroltypeid', 
              'depth', 'thickness', 'notes', 'analysisunitid']
    
    inputs = nh.clean_inputs(nh.pull_params(params, yml_dict, csv_file, 'ndb.chroncontrols'))
    inputs_age = nh.clean_inputs(nh.pull_params(['age'], yml_dict, csv_file, 'ndb.sampleages'))
    agetype = list(set(inputs_age['unitcolumn']))
    inputs['agetype'] = agetype[0]

    if inputs['agetype'] == 'cal yr BP':
        inputs['agetypeid'] = 2
        response.message.append("✔ The provided age type is correct.")
        response.valid.append(True)
    elif inputs['agetype'] == 'CE/BCE':
        inputs['agetypeid'] = 1
        response.message.append("✔ The provided age type is correct.")
        response.valid.append(True)
    else:
        response.message.append("✗ The provided age type is incorrect..")
        response.valid.append(False)
        inputs['agetypeid'] = None
    inputs_age['age'] = [float(value) if value != 'NA' else None for value in inputs_age['age']]
    inputs_age['uncertainty'] = [float(value) if value != 'NA' else None for value in inputs_age['uncertainty']]

    if len(inputs['depth']) == len(inputs_age['age']) == len(inputs['thickness']):
        response.message.append(f"✔ The number of depths (analysis units), ages, and thicknesses are the same.")
        response.valid.append(True)
    else:
        response.message.append(f"✗ The number of depths (analysis units), ages, and thicknesses is not the same. Please check.")
        response.valid.append(False)
    
    for k in inputs:
        if not inputs[k]:
            response.message.append(f'? {k} has no values.')
            response.valid.append(False)
        else:
            response.message.append(f'✔ {k} looks valid.')
            response.valid.append(True)
    if inputs_age['age']:
        age_min = min([x for x in inputs_age['age'] if x is not None])
        age_max = max([x for x in inputs_age['age'] if x is not None])
    else:
        age_min = age_max = None
    for i in range(0, len(inputs['depth'])):
        try:
            ChronControl(chroncontroltypeid = inputs['chroncontrolid'], 
                              depth = inputs['depth'][i], 
                              thickness = inputs['thickness'][i],
                              age = inputs_age['age'], 
                              agelimityounger = age_min, 
                              agelimitolder = age_max,
                              notes = inputs['notes'],
                              agetypeid = inputs['agetypeid'])
            response.valid.append(True)
            response.message.append(f"Can create chron control")
        except Exception as e:
            response.message.append(f"Could not do chron control {e}")
            response.valid.append(False)
    response.validAll = all(response.valid)
    return response