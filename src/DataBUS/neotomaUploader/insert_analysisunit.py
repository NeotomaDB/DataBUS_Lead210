import DataBUS.neotomaHelpers as nh
from DataBUS import AnalysisUnit, AUResponse


def insert_analysisunit(cur, yml_dict, csv_file, uploader):
    """_Inserting analysis units_
    Args:
        cur (_psycopg2.extensions.cursor_): _A cursor pointing to the Neotoma
            Paleoecology Database._
        yml_dict (_dict_): _A `dict` returned by the YAML template._
        csv_file (_dict_): _The csv file with the required data to be uploaded._
        uploader (_dict_): A `dict` object that contains critical information about the
          object uploaded so far.
    Returns:
        _int_: _The integer value of the newly created siteid from the Neotoma Database._
    """
    params = [
        "analysisunitname",
        "depth",
        "thickness",
        "faciesid",
        "mixed",
        "igsn",
        "notes",
        "recdatecreated",
        "recdatemodified",
    ]
    inputs = nh.clean_inputs(
        nh.pull_params(params, yml_dict, csv_file, "ndb.analysisunits")
    )
    response = AUResponse()

    kv = {
        "mixed": False,
        "faciesid": None,
        "igsn": None,
        "notes": None,
        "recdatecreated": None,
        "recdatemodified": None,
    }
    for k in kv:
        if inputs[k] == None:
            inputs[k] = [kv[k]] * len(inputs["depth"])
    for i in range(0, len(inputs["depth"])):
        try:
            au = AnalysisUnit(
                collectionunitid=uploader["collunitid"].cuid,
                analysisunitname=inputs["analysisunitname"],
                depth=inputs["depth"][i],
                thickness=inputs["thickness"][i],
                faciesid=inputs["faciesid"][i],
                mixed=inputs["mixed"][i],
                igsn=inputs["igsn"][i],
                notes=inputs["notes"][i],
                recdatecreated=inputs["recdatecreated"][i],
                recdatemodified=inputs["recdatemodified"][i],
            )
        except Exception as e:
            response.message.append(
                f"✗ Could not create Analysis Unit, " f"verify entries: \n {e}"
            )
            au = AnalysisUnit(collectionunitid=uploader["collunitid"].cuid, mixed=False)
        try:
            auid = au.insert_to_db(cur)
            response.message.append(f"✔ Added Analysis Unit {auid}.")
            response.valid.append(True)
        except Exception as e:
            response.message.append(
                f"✗ Analysis Unit Data is not correct. Error message: {e}"
            )
            au = AnalysisUnit(collectionunitid=uploader["collunitid"].cuid)
            auid = au.insert_to_db(cur)
            response.message.append(
                f"✗ Adding temporary Analysis Unit {auid} to continue process."
                f"\nSite will be removed from upload."
            )
            response.valid.append(False)
        # response.aulist.append(auid)
        response.auid.append(auid)
    response.validAll = all(response.valid)
    return response
