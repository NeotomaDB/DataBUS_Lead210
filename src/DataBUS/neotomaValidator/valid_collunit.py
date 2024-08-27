import itertools
import DataBUS.neotomaHelpers as nh
from DataBUS import Geog, WrongCoordinates, CollectionUnit, CUResponse


def valid_collunit(cur, yml_dict, csv_file):
    """
    Validates whether the specified collection unit can be registered as a new unit in the Neotoma database.

    Args:
        cur (psycopg2.extensions.connection): A database connection object to interact with a Neotoma database, which can be either local or remote.
        yml_dict (dict): A dictionary containing data from a YAML template.
        csv_file (str): The path to a CSV file with the required data to be uploaded.

    Returns:
        CUResponse: An object containing the validation response with the following attributes:
            - valid (bool): Indicates whether the collection unit passed the validation checks.
            - message (list): A list of messages detailing the validation process.
            - culist (list): A list of dictionaries containing site and collection unit names that are valid within the specified site context.
    """
    response = CUResponse()
    params = [
        "handle",
        "core",
        "colltypeid",
        "depenvtid",
        "collunitname",
        "colldate",
        "colldevice",
        "gpsaltitude",
        "gpserror",
        "waterdepth",
        "substrateid",
        "slopeaspect",
        "slopeangle",
        "location",
        "notes",
        "geog",
    ]
    inputs = nh.clean_inputs(
        nh.pull_params(params, yml_dict, csv_file, "ndb.collectionunits")
    )

    for key, value in inputs.items():
        if isinstance(value, list) and len(value) == 1:
            inputs[key] = value[0]
    
    if inputs["depenvtid"]:
        query = """SELECT depenvtid FROM ndb.depenvttypes
                    WHERE LOWER(depenvt) = %(depenvt)s"""
        cur.execute(query, {"depenvt": inputs["depenvtid"].lower()})
        inputs["depenvtid"] = cur.fetchone()[0]

    try:
        geog = Geog((inputs["geog"][0], inputs["geog"][1]))
        response.message.append(
            f"? This set is expected to be " f"in the {geog.hemisphere} hemisphere."
        )
    except (TypeError, WrongCoordinates) as e:
        response.valid.append(False)
        response.message.append(str(e))
        geog = None

    try:
        cu = CollectionUnit(
            handle=inputs["handle"],
            core=inputs["core"],
            colltypeid=inputs["colltypeid"],
            depenvtid=inputs["depenvtid"],
            collunitname=inputs["collunitname"],
            colldate=inputs["colldate"],
            colldevice=inputs["colldevice"],
            gpsaltitude=inputs["gpsaltitude"],
            gpserror=inputs["gpserror"],
            waterdepth=inputs["waterdepth"],
            substrateid=inputs["substrateid"],
            slopeaspect=inputs["slopeaspect"],
            slopeangle=inputs["slopeangle"],
            location=inputs["location"],
            notes=inputs["notes"],
            geog=geog,
        )
        response.valid.append(True)
    except (ValueError, TypeError, Exception) as e:
        response.valid.append(False)
        response.message.append(e)
        cu = CollectionUnit()

    response.message.append(f"Handlename: {cu.handle}")
    if inputs["handle"] != cu.handle:
        response.message.append(
            "? Handlename not given. Handle created from core code."
        )
    cur.execute(
        "SELECT * FROM ndb.collectionunits WHERE LOWER(handle) = %(handle)s;",
        ({"handle": cu.handle.lower()}),
    )
    rows = cur.fetchall()
    if not rows:
        response.message.append("✔  No handle found. Creating a new collection unit.")
        response.valid.append(True)
    else:
        response.message.append("? There is a handle with this handle name.")
        if len(rows) == 1:
            coll_info = rows[0]
            try:
                found_cu = CollectionUnit(
                    collectionunitid=int(coll_info[0]),
                    handle=str(coll_info[1]),
                    siteid=nh.clean_numbers(coll_info[2]),
                    colltypeid=nh.clean_numbers(coll_info[3]),
                    depenvtid=nh.clean_numbers(coll_info[4]),
                    collunitname=str(coll_info[5]),
                    colldate=coll_info[6],
                    colldevice=str(coll_info[7]),
                    geog=Geog(
                        (nh.clean_numbers(coll_info[8]), nh.clean_numbers(coll_info[9]))
                    ),
                    gpsaltitude=nh.clean_numbers(coll_info[10]),
                    gpserror=coll_info[11],
                    waterdepth=nh.clean_numbers(coll_info[12]),
                    substrateid=coll_info[13],
                    slopeaspect=coll_info[14],
                    slopeangle=coll_info[15],
                    location=str(coll_info[16]),
                    notes=str(coll_info[17]),
                )
                msg = cu.compare_cu(found_cu)
                response.message.append(f"? CU equal: {cu == found_cu}.")
                response.message.append(f"{msg}")

            except Exception as e:
                response.message.append(e)
            
    close_handles = cu.find_close_collunits(cur)
    if len(close_handles) > 0:
        goodcols = [i[-2] for i in close_handles]
        if any([j == cu.handle for j in goodcols]):
            response.message.append(
                f"" #Collection unit was found - but this would also happen from the above search
            )
        else:
            response.message.append(
                f"?  The collection unit handle does not occur "
                f"within close sites."
            )
            sitecol = itertools.groupby(
                [{"sitename": k[1], "collunit": k[-2]} for k in close_handles],
                lambda x: x["sitename"],
            )
            sitemsg = [
                {"site": key, "collunits": [k["collunit"] for k in list(value)]}
                for key, value in sitecol
            ]
            for i in sitemsg:
                site = {"site": i["site"], "collunits": i["collunits"]}
                response.culist.append(site)
    else:
        response.message.append(
            f"✔  There are no nearby sites, a new collection unit "
            f"will be created."
        )
        response.valid.append(True)

    response.validAll = all(response.valid)
    return response
