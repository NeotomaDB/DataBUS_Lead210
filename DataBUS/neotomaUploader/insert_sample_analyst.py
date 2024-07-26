import DataBUS.neotomaHelpers as nh
from DataBUS import Response, Contact

def insert_sample_analyst(cur, yml_dict, csv_file, uploader):
    """
    Inserts sample analyst data into Neotoma

    Args:
        cur (cursor object): Database cursor to execute SQL queries.
        yml_dict (dict): Dictionary containing YAML data.
        csv_file (str): File path to the CSV template.
        uploader (dict): Dictionary containing uploader details.

    Returns:
        response (dict): A dictionary containing information about the inserted sample analysts.
            - 'contids' (list): List of dictionaries containing details of the analysts' IDs.
            - 'valid' (bool): Indicates if all insertions were successful.
    """
    response = Response()
    params = ['contactid']
    inputs = nh.pull_params(params, yml_dict, csv_file, 'ndb.sampleanalysts')

    inputs['contactid'] = list(dict.fromkeys(inputs['contactid']))
    contids = nh.get_contacts(cur, inputs['contactid'])

    for i in range(len(uploader['samples'].sampleid)):
        for contact in contids:
            try:
                agent = Contact(contactid = int(contact['id']),
                                order = int(contact['order']))
                response.valid.append(True)
            except Exception as e:
                agent = Contact(contactid=contact['id']),
                response.message.append(f"✗ Sample Analyst data is not correct. {e}")
                response.valid.append(False)
            finally:
                try:
                    agent.insert_sample_analyst(cur, sampleid=int(uploader['samples'].sampleid[i]))
                    response.valid.append(True)
                    response.message.append(f"✔  Sample Analyst {contact['id']} added "
                                            f"for sample {uploader['samples'].sampleid[i]}.")
                except:
                    response.message.append(f"Executed temporary query.")
                    response.valid.append(False)
                response.valid.append(False)

    response.valid = all(response.valid)
    return response