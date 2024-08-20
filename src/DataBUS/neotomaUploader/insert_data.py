import DataBUS.neotomaHelpers as nh
from DataBUS import Response, Datum, Variable


def insert_data(cur, yml_dict, csv_file, uploader):
    """"""
    response = Response()

    params = ["value"]
    inputs = nh.pull_params(params, yml_dict, csv_file, "ndb.data")
   # print(inputs)

    params2 = ["variableelementid", "variablecontextid"]
    inputs2 = nh.clean_inputs(nh.pull_params(params2, yml_dict, csv_file, "ndb.data"))
    inputs2 = {
        p: (
            [None] * len(uploader["samples"].sampleid)
            if inputs2[p] is None
            else inputs2[p]
        )
        for p in params2
    }

    data_id = []
    counter_ = 0
    uncertainty_d = []
    for val_dict in inputs:
        data_id_u = []
        var_id = []
        counter = 0
        for i in range(len(uploader["samples"].sampleid)):
            counter_ += 1
            get_taxonid = (
                """SELECT * FROM ndb.taxa WHERE LOWER(taxonname) = %(taxonname)s;"""
            )
            cur.execute(get_taxonid, {"taxonname": val_dict["taxonname"].lower()})
            taxonid = cur.fetchone()

            if taxonid:
                taxonid = int(taxonid[0])
            else:
                counter += 1
                taxonid = counter  # To do temporary taxon
                response.message.append(
                    f"✗  Taxon ID for {val_dict['taxonname']} not found."
                    f"Does it exist in Neotoma?"
                )
                response.valid.append(False)

            val_dict["value"] = [
                None if item == "NA" else item for item in val_dict["value"]
            ]

            # Get UnitsID
            get_vunitsid = """SELECT variableunitsid FROM ndb.variableunits 
                             WHERE LOWER(variableunits) = %(units)s;"""
            cur.execute(get_vunitsid, {"units": val_dict["unitcolumn"][i].lower()})
            vunitsid = cur.fetchone()[0]  # This is just getting the varunitsid
            counter2 = 0
            if vunitsid:
                vunitsid = int(vunitsid)
                response.message.append(f"✔ Units ID {vunitsid} found.")
            else:
                counter2 += 1
                vunitsid = counter
                response.message.append(
                    f"✗  UnitsID for {val_dict['unitcolumn'][i].lower()} "
                    f"not found. \nDoes it exist in Neotoma?"
                    f"Temporary UnitsID {vunitsid} for insert."
                )
                response.valid.append(False)

            try:
                var = Variable(
                    variableunitsid=vunitsid,
                    taxonid=taxonid,
                    variableelementid=inputs2["variableelementid"][i],
                    variablecontextid=inputs2["variablecontextid"][i],
                )
                response.valid.append(True)
            except Exception as e:
                var = Variable(
                    variableunitsid=vunitsid,
                    taxonid=taxonid,
                    variableelementid=None,
                    variablecontextid=None,
                )
                response.valid.append(False)
                response.message.append(f"✗  Variable cannot be created: {e}")
            finally:
                try:
                    varid = var.get_id_from_db(cur)
                    response.valid.append(True)
                except Exception as e:
                    response.valid.append(False)
                    response.message.append(
                        f"✗  Var ID cannot be retrieved from db: {e}"
                    )
                    varid = None

            if varid:
                varid = varid[0]
                response.valid.append(True)
                response.message.append(f"✔ Var ID {varid} found.")
            else:
                response.message.append(
                    "? Var ID not found. Executing ts.insertvariable"
                )
                varid = var.insert_to_db(cur)

            try:
                datum = Datum(
                    sampleid=int(uploader["samples"].sampleid[i]),
                    variableid=int(varid),
                    value=val_dict["value"][i],
                )
                response.valid.append(True)
            except Exception as e:
                response.valid.append(False)
                response.message.append(f"✗  Datum cannot be created: {e}")
                varid = None
                datum = Datum(
                    sampleid=int(uploader["samples"].sampleid[i]),
                    variableid=varid,
                    value=None,
                )
            finally:
                var_id.append(varid)
                try:
                    d_id = datum.insert_to_db(cur)
                    response.valid.append(True)
                    response.message.append(f"✔ Added Datum {d_id}")
                except Exception as e:
                    response.valid.append(False)
                    response.message.append(f"✗  Datum cannot be inserted: {e}")
                    d_id = 2
                finally:
                    response.data_id.append(d_id)
                    data_id_u.append(d_id)
        if "uncertainty" in val_dict:
            response.uncertaintyinputs.append({"varid": var_id, "dataid": data_id_u})

    response.validAll = all(response.valid)
    return response
