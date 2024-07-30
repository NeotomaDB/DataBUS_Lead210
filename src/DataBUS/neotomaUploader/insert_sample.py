import DataBUS.neotomaHelpers as nh
from DataBUS import Sample, Response


def insert_sample(cur, yml_dict, csv_file, uploader):
    """
    Inserts sample data into Neotoma.

    Args:
        cur (cursor object): Database cursor to execute SQL queries.
        yml_dict (dict): Dictionary containing YAML data.
        csv_file (str): File path to the CSV template.
        uploader (dict): Dictionary containing uploader details.

    Returns:
        response (dict): A dictionary containing information about the inserted samples.
            - 'samples' (list): List of sample IDs inserted into the database.
            - 'valid' (bool): Indicates if all insertions were successful.
    """
    response = Response()
    params = [
        "sampledate",
        "analysisdate",
        "prepmethod",
        "notes",
        "taxonname",
        "samplename",
    ]
    inputs = nh.clean_inputs(nh.pull_params(params, yml_dict, csv_file, "ndb.samples"))
    inputs["labnumber"] = nh.retrieve_dict(yml_dict, "ndb.samples.labnumber")
    inputs["labnumber"] = inputs["labnumber"][0]["value"]

    for j in range(len(uploader["anunits"].auid)):
        get_taxonid = """SELECT * FROM ndb.taxa WHERE taxonname %% %(taxonname)s;"""
        cur.execute(get_taxonid, {"taxonname": inputs["taxonname"]})
        taxonid = cur.fetchone()
        if taxonid != None:
            taxonid = int(taxonid[0])
        else:
            taxonid = None
        try:
            sample = Sample(
                analysisunitid=uploader["anunits"].auid[j],
                datasetid=uploader["datasetid"].datasetid,
                samplename=inputs["samplename"],
                sampledate=inputs["sampledate"],
                analysisdate=inputs["analysisdate"],
                taxonid=taxonid,
                labnumber=inputs["labnumber"],
                prepmethod=inputs["prepmethod"],
                notes=inputs["notes"],
            )
            response.valid.append(True)

        except Exception as e:
            sample = Sample()
            response.message.append(f"✗ Samples data is not correct: {e}")
            response.valid.append(False)
        finally:
            try:
                s_id = sample.insert_to_db(cur)
                response.sampleid.append(s_id)
                response.valid.append(True)
                response.message.append(f"✔  Added Sample {s_id}.")
            except Exception as e:
                s_id = sample.insert_to_db(cur)
                response.sampleid.append(s_id)
                response.valid.append(True)
                response.message.append(f"✗  Cannot add sample: {e}.")

    if not len(uploader["anunits"].auid) == len(response.sampleid):
        response.message.append(
            "✗  Analysis Units and Samples do not have same length."
        )
    response.validAll = all(response.valid)
    return response
