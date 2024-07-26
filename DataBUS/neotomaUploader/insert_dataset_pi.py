from DataBUS import Response, Contact
import DataBUS.neotomaHelpers as nh

def insert_dataset_pi(cur, yml_dict, csv_file, uploader):
    """
    Inserts dataset principal investigator data into Neotomas.

    Args:
        cur (cursor object): Database cursor to execute SQL queries.
        yml_dict (dict): Dictionary containing YAML data.
        csv_file (str): File path to the CSV template.
        uploader (dict): Dictionary containing uploader details.

    Returns:
        response (dict): A dictionary containing information about the inserted dataset principal investigators.
            - 'dataset_pi_ids' (list): List of dictionaries containing details of the contacts, including their IDs and order.
            - 'valid' (bool): Indicates if all insertions were successful.
    """
    response = Response()
    inputs = nh.pull_params(['contactid'], yml_dict, csv_file, 'ndb.datasetpis')

    # Use this method to preserve order.
    inputs['contactid'] = list(dict.fromkeys(inputs['contactid']))
    contids = nh.get_contacts(cur, inputs['contactid'])
    for agent in contids:
        try:
            contact = Contact(contactid = int(agent['id']),
                              order = int(agent['order']))
            response.valid.append(True)
        except Exception as e:
            contact = Contact(contactid = None,
                              order = None)
            response.message.append(f"✗ Contact DatasetPI is not correct. {e}")
            response.valid.append(False)
        finally:
            try:
                contact.insert_pi(cur, uploader['datasetid'].datasetid)
                response.message.append(f"✔ Added PI {agent['id']}.")
            except Exception as e:
                response.message.append(f"✗ DatasetPI cannot be added. {e}")
                response.valid.append(False)

    response.datasetpi = contids
    response.validAll = all(response.valid)
    return response