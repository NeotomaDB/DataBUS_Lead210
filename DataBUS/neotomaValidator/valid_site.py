from DataBUS.neotomaHelpers.pull_params import pull_params
import DataBUS.neotomaHelpers as nh
from DataBUS import Geog, WrongCoordinates, Site, SiteResponse

def valid_site(cur, yml_dict, csv_file):
    """
    Validate if the provided site details correspond to a new and valid site entry.

    This function checks the validity of a site based on its coordinates, name, and hemisphere. It returns a dictionary containing:
        * `pass`: Boolean indicating if the site validation was successful.
        * `sitelist`: List of dictionaries for sites that are close to the provided coordinates. Each dictionary includes 'siteid', 'sitename', 'lat', 'long', and 'distance'.
        * `hemisphere`: String indicating the hemisphere of the site based on its coordinates.
        * `matched`: Dictionary with details about name and distance matching with nearby sites, including:
            * `namematch`: Boolean indicating if a nearby site has the same name as the provided site.
            * `distmatch`: Boolean indicating if a nearby site's coordinates exactly match the provided coordinates.

    Args:
        cur (_psycopg2.extensions.connection_): Database connection to a Neotoma database.
        coords (list): Coordinates of the site, expected as [latitude, longitude].
        hemisphere (list): List of strings representing acceptable hemispheres (e.g., ['NW', 'NE', 'SW', 'SE']).
        sitename (str): The unique name of the site.

    Returns:
        dict: Contains the keys `pass`, `sitelist`, `hemisphere`, and `matched` with respective validation results.
    """
    response = {'valid': [],
                'hemisphere': '', 
                'sitelist': [],
                'matched': {'namematch': False, 'distmatch': False},
                'doublematch':False,
                'message': []}
    response = SiteResponse()
    params = ["siteid", "sitename", "altitude", "area", "sitedescription", "notes", "geog"]
    inputs = pull_params(params, yml_dict, csv_file, 'ndb.sites')
    inputs = nh.clean_inputs(inputs)
    overwrite = nh.pull_overwrite(params, yml_dict, 'ndb.collectionunits')

    try:
        geog = Geog((inputs['geog'][0], inputs['geog'][1]))
        response.message.append(f"? This set is expected to be "
                                   f"in the {geog.hemisphere} hemisphere.")
    except TypeError as e:
        response.valid.append(False)
        response.message.append(e)
        geog = None
    except WrongCoordinates as e:
        response.valid.append(False)
        response.message.append(e)
        geog = None

    try:
        site = Site(siteid=inputs['siteid'],
                    sitename = inputs['sitename'],
                    altitude = inputs['altitude'],
                    area = inputs['area'],
                    sitedescription= inputs['sitedescription'],
                    notes = inputs['notes'],
                    geog = geog)
    except ValueError as e:
        response.valid.append(False)
        response.message.append(e)
        site = Site()
    except TypeError as e:
        response.valid.append(False)
        response.message.append(e)
        site = Site()
    except Exception as e:
        response.valid.append(False)
        response.message.append(e)
        site = Site()

    # When not given a SiteID
    site.siteid = None
    if site.siteid is None:
        close_sites = site.find_close_sites(cur)
        if close_sites:
            response.message.append('?  One or more sites exist close to the requested site.')
            for site_data in close_sites:
                new_site = Site(siteid = site_data[0],
                                sitename = site_data[1],
                                geog = Geog((site_data[3], site_data[2])))
                new_site.distance = round(site_data[13], 0)
                response.closesites.append(new_site)
            sitenames_list = [site.sitename for site in response.closesites]
            response.matched['namematch'] = any(name in sitenames_list for name in site.sitename)
            response.matched['distmatch'] = any(site.distance == 0 for site in response.closesites)
            response.doublematched = response.matched['namematch'] and response.matched['distmatch']
            match_status = 'matches' if response.doublematched else 'differs'
            response.message.append(f'? Site name {match_status}, but locations differ.')
        else:
            response.valid.append(True)
            response.sitelist = [Site()]
            response.message.append('✔  There are no sites close to the proposed site.')
    else:
        response.message.append("Verifying if the site exists already in neotoma with the same siteID")
        site_query = """SELECT * from ndb.sites where siteid = %(siteid)s"""
        cur.execute(site_query, {'siteid': site.siteid})
        site_info = cur.fetchall()
        if not site_info:
            response.valid.append(False)
            response.message.append(f"? Site ID {site.siteid} is not currently associated to a site in Neotoma.")
        else:
            response.message.append("✔  Site ID found in Neotoma:")
            for site_data in site_info:
                new_site = Site(siteid = site_data[0],
                            sitename = site_data[1],
                            geog = Geog((site_data[3],site_data[2])))
                response.sitelist.append(site)
                name_match = site.sitename[0] == new_site.sitename
                coord_match = site.geog == new_site.geog
                response.matched['namematch'] = name_match
                response.matched['distmatch'] = coord_match
                response.valid.append(name_match)
                response.message.append(new_site)
                if not name_match:
                    response.message.append(f"✗ The sitenames do not match. Current sitename in Neotoma: {site['name']}. Proposed name: {inputs['sitename'][0]}.")
                else:
                    response.message.append("✔  Names match")
                if not coord_match:
                    close_sites = site.find_close_sites(cur, limit = 3)
                    for site_data in close_sites:
                        close_site = Site(siteid = site_data[0],
                                        sitename = site_data[1],
                                        geog = Geog((site_data[3], site_data[2])))
                        new_site.distance = round(site_data[13], 0)
                        response.closesites.append(close_site)
                    if not overwrite['geog']:
                        response.message.append(f"? Coordinates do not match."
                                                   f"Neotoma coordinates will stay in place. \n"
                                                   f"Current coords in Neotoma: {new_site.geog}. \n" 
                                                   f"Proposed coords: {site.geog}.")
                    else:
                        response.message.append("? Coordinates do not match. "
                                                   f"Proposed coordinates will stay in place. \n"
                                                   f"Current coords in Neotoma: {new_site.geog}. \n" 
                                                   f"Proposed coords: {site.geog}.")
                else:
                    response.message.append("✔  Coordinates match")

    response.validAll = all(response.valid)
    print(response)
    return response