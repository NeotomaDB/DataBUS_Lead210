import DataBUS.neotomaHelpers as nh
from DataBUS import Dataset, Response

def valid_dataset(cur, yml_dict, csv_file):
    """_Validating Datasets_"""
    response = Response()
    
    inputs = {'datasetname': 
              nh.retrieve_dict(yml_dict, 'ndb.datasets.datasetname')[0]['value'].lower(),
              'datasettypeid': 
              nh.retrieve_dict(yml_dict, 'ndb.datasettypes.datasettypeid')[0]['value'].lower()}
    response.message.append(f"Datasettype: {inputs['datasetname']}")
    inputs['notes'] = nh.clean_inputs(nh.pull_params(['notes'], yml_dict, csv_file, 'ndb.datasets'))

    query = "SELECT DISTINCT datasettypeid FROM ndb.datasettypes"
    cur.execute(query)
    all_datasets = cur.fetchall()
    all_datasets = [value[0] for value in all_datasets]

    query = "SELECT datasettypeid FROM ndb.datasettypes WHERE LOWER(datasettype) = %(ds_type)s"
    cur.execute(query,{'ds_type': inputs['datasettypeid']})
    if inputs['datasettypeid']:
        inputs['datasettypeid'] = inputs['datasettypeid'][0]

    if inputs['datasettypeid'] in all_datasets:
        response.message.append("✔ Dataset type exists in neotoma.")
        response.valid.append(True)
    else:
        response.message.append(f"✗ Dataset type is not known to neotoma. Add it first")
        response.valid.append(False)

    try:
        Dataset(datasettypeid = None, 
                 datasetname = inputs['datasetname'], 
                 notes = inputs['notes'])
        response.message.append(f"✔ Dataset can be created.")
        response.valid.append(True)
    except Exception as e:
        response.message.append(f"✗ Dataset cannot be created: {e}")
        response.valid.append(False)
    
    response.validAll = all(response.valid)
    
    return response