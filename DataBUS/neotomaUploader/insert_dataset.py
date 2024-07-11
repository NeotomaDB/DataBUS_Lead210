import DataBUS.neotomaHelpers as nh
from DataBUS import Dataset, Response

def insert_dataset(cur, yml_dict, csv_file, uploader):
    """
    Inserts a dataset associated with a collection unit into a database.

    Args:
        cur (cursor object): Database cursor to execute SQL queries.
        yml_dict (dict): Dictionary containing YAML data.
        csv_file (str): File path to the CSV template.
        uploader (dict): Dictionary containing uploader details.

    Returns:
        response (dict): A dictionary containing information about the inserted dataset.
            'datasetid' (int): IDs for the inserted dataset.
            'valid' (bool): Indicates if insertions were successful.
    """
    response = Response()
    
    inputs = {'datasetname': 
              nh.retrieve_dict(yml_dict, 'ndb.datasets.datasetname')[0]['value'].lower(),
              'datasettypeid': 
              nh.retrieve_dict(yml_dict, 'ndb.datasettypes.datasettypeid')[0]['value'].lower()}
    
    inputs['notes'] = nh.clean_inputs(nh.pull_params(['notes'], yml_dict, csv_file, 
                                                     'ndb.datasets'))['notes']
    query = "SELECT datasettypeid FROM ndb.datasettypes WHERE LOWER(datasettype) = %(ds_type)s"
    cur.execute(query,{'ds_type': inputs['datasettypeid'].lower()})
    if inputs['datasettypeid']:
        inputs['datasettypeid'] = cur.fetchone()[0]

    try:
        ds = Dataset(datasettypeid = inputs['datasettypeid'],
                     collectionunitid = uploader['collunitid'].cuid,
                     datasetname = inputs['datasetname'],
                     notes = inputs['notes'])
        
        response.valid.append(True)
        response.message.append("✔ Dataset was created.")
    except Exception as e:
        print(e)
        response.valid.append(False)
        response.message.append("✗ Dataset was not created: {e}")
        ds = Dataset(datasettypeid = 10,
                     collectionunitid = uploader['collunitid'].cuid,)
    finally:
        try:
            response.datasetid = ds.insert_to_db(cur)
            response.valid.append(True)
            response.message.append(f"✔ Dataset {response.datasetid} added to Neotoma.")
        except Exception as e:
            response.datasetid = ds.insert_to_db(cur)
            response.valid.append(True)
            response.message.append(f"✗ Dataset {response.datasetid} was not added to Neotoma."
                                    f"Using temporary ID.")
    response.validAll = all(response.valid)
    return response 