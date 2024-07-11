import DataBUS.neotomaHelpers as nh
from DataBUS import Response, DatasetDatabase

def insert_dataset_database(cur, yml_dict, uploader):
    """
    Inserts dataset and database associations into Neotoma

    Args:
        cur (cursor object): Database cursor to execute SQL queries.
        yml_dict (dict): Dictionary containing YAML data.
        uploader (dict): Dictionary containing uploader details.

    Returns:
        response (dict): A dictionary containing information about the dataset-database insertion.
            - 'databaseid' (int): ID of the associated database or NaN if not available.
            - 'valid' (bool): Indicates if the insertion was successful.
    """
    response = Response()

    db_name = nh.retrieve_dict(yml_dict, 'ndb.datasetdatabases.databaseid')
    inputs = {'databaseid': db_name[0]['value']}

    try:
        db = DatasetDatabase(datasetid = int(uploader['datasetid'].datasetid), 
                        databaseid = int(inputs['databaseid']))
        response.valid.append(True)
        response.message.append(f"✔ Database ID {inputs['databaseid']} created.")
    except Exception as e:
        db = DatasetDatabase(datasetid = int(uploader['datasetid'].datasetid))
        response.message.append(f"✗ Database information is not correct. {e}")
        response.valid.append(False)
    finally:
        try:
            db.insert_to_db(cur)
            response.valid.append(True)
            response.message.append(f"✔ Database ID {inputs['databaseid']} inserted.")
        except Exception as e:
            response.message.append(f"✗ Cannot upload DatasetDatabase: {e}")
            response.valid.append(False)

    response.databaseid = inputs['databaseid']
    response.validAll = all(response.valid)
    return response