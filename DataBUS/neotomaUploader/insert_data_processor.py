from DataBUS import Contact, Response
import DataBUS.neotomaHelpers as nh

def insert_data_processor(cur, yml_dict, csv_file, uploader):
    """
    Inserts data processors into Neotoma

    Args:
        cur (cursor object): Database cursor to execute SQL queries.
        yml_dict (dict): Dictionary containing YAML data.
        csv_file (str): File path to the CSV template.
        uploader (dict): Dictionary containing uploader details.

    Returns:
        response (dict): A dictionary containing information about the inserted data processors.
            - 'processorid' (list): List of processors' IDs.
            - 'valid' (bool): Indicates if all insertions were successful.
    """
    response = Response()
    inputs = nh.pull_params(['contactid'], yml_dict, csv_file, 'ndb.sampleanalysts')

    # Use this method to preserve order.
    inputs['contactid'] = list(dict.fromkeys(inputs['contactid']))
    contids = nh.get_contacts(cur, inputs['contactid'])
    params = ['contactid']
    inputs = nh.pull_params(params, yml_dict, csv_file, 'ndb.sampleanalysts')
    
    for contact in contids:
        try:
            agent = Contact(contactid = contact['id'])
            response.valid.append(True)
            response.message.append(f"✔ Processor object {contact['id']} created.")
        except Exception as e:
            agent = Contact(contactid = 1)
            response.valid.append(False)
            response.message.append(f"Creating temporary insert object: {e}")
        finally:
            try:
                agent.insert_data_processor(cur, datasetid=uploader['datasetid'].datasetid)
                response.valid.append(True)
                response.message.append(f"✔ Processor {contact['id']} inserted.")
            except Exception as e:
                response.message.append(f"✗ Data processor information is not correct. {e}")
                response.valid.append(False)

    response.processor = contids
    response.validAll = all(response.valid)
    return response