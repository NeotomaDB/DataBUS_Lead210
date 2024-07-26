import DataBUS.neotomaHelpers as nh
from DataBUS import ChronControl, ChronResponse

def insert_chron_control(cur, yml_dict, csv_file, uploader):
    """
    Inserts chronological control data into a database.

    Args:
        cur (cursor object): Database cursor to execute SQL queries.
        yml_dict (dict): Dictionary containing YAML data.
        csv_file (str): File path to the CSV template.
        uploader (dict): Dictionary containing uploader details.

    Returns:
        response (dict): A dictionary containing information about the inserted chronological control units.
            'chron_control_units' (list): List of IDs for the inserted chronological control units.
            'valid' (bool): Indicates if all insertions were successful.

    Raises:
        AssertionError: If the number of analysis units, ages, and thicknesses are not consistent.
    """
    response = ChronResponse()
    params = ['chroncontrolid', 'chronologyid', 'chroncontroltypeid', 
              'depth', 'thickness', 'notes', 'analysisunitid']
    
    inputs = nh.clean_inputs(nh.pull_params(params, yml_dict, csv_file, 'ndb.chroncontrols'))
    inputs_age = nh.clean_inputs(nh.pull_params(['age'], yml_dict, csv_file, 'ndb.sampleages'))
    agetype = list(set(inputs_age['unitcolumn']))
    inputs['agetype'] = agetype[0]

    #inputs_age['age'] = [float(value) if value != 'NA' else None for value in inputs_age['age']]
    inputs_age['uncertainty'] = [float(value) if value != 'NA' else None for value in inputs_age['uncertainty']]
    agetype = list(set(inputs_age['unitcolumn']))
    agetype = agetype[0]

    assert len(uploader['anunits'].auid) == len(inputs_age['age']) == len(inputs['thickness']), \
           "The number of analysis units, ages, and thicknesses is not the same. Please check."

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
    
    if inputs_age['age']:
        age_min = min([x for x in inputs_age['age'] if x is not None])
        age_max = max([x for x in inputs_age['age'] if x is not None])
    else:
        age_min = age_max = None
    for k in ['notes']:
        if inputs[k] == None:
            inputs[k] = [inputs[k]] * len(inputs['depth'])
    
    for i in range(len(uploader['anunits'].auid)):
        try:
            cc = ChronControl(chronologyid= int(uploader['chronology'].chronid),
                              analysisunitid= int(uploader['anunits'].auid[i]),
                              chroncontroltypeid = inputs['chroncontrolid'], 
                              depth = inputs['depth'][i], 
                              thickness = inputs['thickness'][i],
                              age = inputs_age['age'][i], 
                              agelimityounger = age_min, 
                              agelimitolder = age_max,
                              notes = inputs['notes'][i],
                              agetypeid = inputs['agetypeid'])
            ccid = cc.insert_to_db(cur)
            response.ccid.append(ccid)
            response.valid.append(True)
            response.message.append(f"✔ Adding Chron Control {ccid}.")

        except Exception as e:
            response.message.append(f"Chron Control Data is not correct. Error message: {e}")
            cc = ChronControl(chronologyid= int(uploader['chronology'].chronid),
                              analysisunitid= int(uploader['anunits'].auid[i]))
            ccid = cc.insert_to_db(cur)
            response.ccid.append(ccid)
            response.message.append(f"✗ Adding temporary chron controls {ccid}.")
            response.valid.append(False)
    response.valid = all(response.valid)
    return response