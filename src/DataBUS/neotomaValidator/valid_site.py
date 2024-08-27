import DataBUS.neotomaHelpers as nh
from DataBUS import Geog, WrongCoordinates, Site, SiteResponse


def valid_site(cur, yml_dict, csv_file):
    """
    Validate if the provided site details correspond to a new and valid site entry.

    This function checks the validity of a site based on its coordinates, name, and other attributes.
    It returns a SiteResponse object containing:
        - `valid`: Boolean indicating if the site validation was successful.
        - `sitelist`: List of Site objects that are close to the provided coordinates.
        - `hemisphere`: String indicating the hemisphere of the site based on its coordinates.
        - `matched`: Dictionary with details about name and distance matching with nearby sites, including:
            - `namematch`: Boolean indicating if a nearby site has the same name as the provided site.
            - `distmatch`: Boolean indicating if a nearby site's coordinates exactly match the provided coordinates.
        - `message`: List of messages detailing the validation process.

    Args:
        cur (_psycopg2.extensions.connection_): Database connection to a Neotoma database.
        yml_dict (dict): Dictionary containing parameters from YAML configuration.
        csv_file (str): Path to CSV file containing additional parameters.

    Returns:
        SiteResponse: Contains the results of the site validation.
    """

    response = SiteResponse()
    params = [
        "siteid",
        "sitename",
        "altitude",
        "area",
        "sitedescription",
        "notes",
        "geog",
    ]
    inputs = nh.clean_inputs(nh.pull_params(params, yml_dict, csv_file, "ndb.sites"))
    overwrite = nh.pull_overwrite(params, yml_dict, "ndb.sites")

    try:
        assert all(
            inputs.get(key) is not None and inputs[key] != []
            for key in ["sitename", "geog"]
        )
    except AssertionError:
        response.message.append(
            f"✗ The template must contain a sitename and coordinates."
        )
        response.valid.append(False)

    try:
        geog = Geog((inputs["geog"][0], inputs["geog"][1]))
        response.message.append(
            f"? This set is expected to be " f"in the {geog.hemisphere} hemisphere."
        )
    except (TypeError, WrongCoordinates) as e:
        response.valid = False
        response.message.append(str(e))
        geog = None

    try:
        # site = Site(**inputs, geog=geog)
        site = Site(
            siteid=inputs["siteid"],
            sitename=inputs["sitename"],
            altitude=inputs["altitude"],
            area=inputs["area"],
            sitedescription=inputs["sitedescription"],
            notes=inputs["notes"],
            geog=geog,
        )
    except (ValueError, TypeError, Exception) as e:
        response.valid.append(False)
        response.message.append(e)
        site = Site()

    if site.siteid is None:
        close_sites = site.find_close_sites(cur)
        if close_sites:
            response.message.append(
                "?  One or more sites exist close to the requested site."
            )
            for site_data in close_sites:
                new_site = Site(
                    siteid=site_data[0],
                    sitename=site_data[1],
                    geog=Geog((site_data[3], site_data[2])),
                )
                new_site.distance = round(site_data[13], 0)
                response.closesites.append(new_site)
            sitenames_list = [site.sitename for site in response.closesites]
            response.matched["namematch"] = any(
                name in sitenames_list for name in site.sitename
            )
            response.matched["distmatch"] = any(
                site.distance == 0 for site in response.closesites
            )
            response.doublematched = (
                response.matched["namematch"] and response.matched["distmatch"]
            )
            match_status = "matches" if response.doublematched else "differs"
            response.message.append(
                f"? Site name {match_status}. Locations differ."
            )
        else:
            response.valid.append(True)
            response.closesites = [Site()]
            response.message.append("✔  There are no sites close to the proposed site.")
    else:
        response.message.append(
            "Verifying if the site exists already in neotoma with the same siteID"
        )
        site_query = """SELECT * from ndb.sites where siteid = %(siteid)s"""
        cur.execute(site_query, {"siteid": site.siteid})
        site_info = cur.fetchall()
        if not site_info:
            response.valid.append(False)
            response.message.append(
                f"? Site ID {site.siteid} is not currently associated to a site in Neotoma."
            )
        else:
            response.message.append("✔  Site ID found in Neotoma:")
            for site_data in site_info:
                new_site = Site(
                    siteid=site_data[0],
                    sitename=site_data[1],
                    geog=Geog((site_data[3], site_data[2])),
                )
                response.matched["namematch"] = site.sitename == new_site.sitename
                response.matched["distmatch"] = site.geog == new_site.geog
                response.valid.append(response.matched["namematch"])
                response.message.append(new_site)
                if not response.matched["namematch"]:
                    response.message.append(
                        f"✗ The sitenames do not match. Current sitename in Neotoma: {site.sitename}. Proposed name in file: {inputs['sitename'][0]}."
                    )
                else:
                    response.message.append("✔  Names match")
                if not response.matched["distmatch"]:
                    close_sites = site.find_close_sites(cur, limit=3)
                    response.message.append(
                        f"? Following sites are close to proposed sites."
                    )
                    for site_data in close_sites:
                        close_site = Site(
                            siteid=site_data[0],
                            sitename=site_data[1],
                            geog=Geog((site_data[3], site_data[2])),
                        )
                        close_site.distance = round(site_data[13], 0)
                        response.closesites.append(close_site)
                    if not overwrite["geog"]:
                        response.message.append(
                            f"? Coordinates do not match."
                            f"Neotoma coordinates will stay in place. \n"
                            f"Current coords in Neotoma: {new_site.geog}. \n"
                            f"Proposed coords: {site.geog}."
                        )
                    else:
                        response.message.append(
                            "? Coordinates do not match. "
                            f"Proposed coordinates will stay in place. \n"
                            f"Current coords in Neotoma: {new_site.geog}. \n"
                            f"Proposed coords: {site.geog}."
                        )
                else:
                    response.message.append("✔  Coordinates match")

    response.validAll = all(response.valid)
    return response
