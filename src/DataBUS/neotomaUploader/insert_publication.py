import DataBUS.neotomaHelpers as nh
from DataBUS import Publication, Response
import requests
import re


def insert_publication(cur, yml_dict, csv_file, uploader):
    """
    Inserts publication data into Neotoma.

    
    """
    response = Response()

    params = [
        "doi",
    ]
    inputs = nh.clean_inputs(
        nh.pull_params(params, yml_dict, csv_file, "ndb.publications")
    )
    
    doi_pattern = r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$"

    #inputs['doi'][0] = "10.1038/nature12373" #placeholder for trial.
    
    if isinstance(inputs['doi'], list):
        if re.match(doi_pattern, inputs['doi'][0], re.IGNORECASE):
            response.message.append(f"✔  DOI is correctly formatted.")
            response.valid.append(True)

            url = f"https://api.crossref.org/works/{inputs['doi'][0]}"
            request = requests.get(url)
            if request.status_code == 200:
                response.message.append(f"✔  DOI {inputs['doi']} found in CrossRef")
                response.valid.append(True)
                data = request.json()
                data = data['message']
            else:
                response.message.append(f"✗  No DOI {inputs['doi']} found in CrossRef")
                data = None
            try:
                pub_type = data['type']
                sql_neotoma = """SELECT pubtypeid FROM ndb.publicationtypes
                                 WHERE LOWER(REPLACE(pubtype, ' ', '-')) LIKE %(pub_type)s
                                 LIMIT 1"""
                cur.execute(sql_neotoma, {'pub_type': pub_type.lower()})
                pubtypeid = cur.fetchone()
                if pubtypeid:
                    pubtypeid = pubtypeid[0]

                pub = Publication(pubtypeid = pubtypeid,
                                  year = None,
                                  citation = None,
                                  title = data['title'][0],
                                  journal = data['container-title'][0],
                                  vol = data['volume'],
                                  issue = data['journal-issue']['issue'],
                                  pages = data['page'],
                                  citnumber = str(data['is-referenced-by-count']),
                                  doi = data['DOI'],
                                  booktitle = None,
                                  numvol = data['volume'],
                                  edition = None,
                                  voltitle = None,
                                  sertitle = None,
                                  servol = None,
                                  publisher = data['publisher'],
                                  url = data['URL'],
                                  city = None,
                                  state = None,
                                  country = None,
                                  origlang = data['language'],
                                  notes = None)
                response.valid.append(True)
            except Exception as e:
                print(e)
                response.valid.append(False)
                response.message.append("✗  Publication cannot be created {e}")
                #pub = Publication()

            try:
                pubid = pub.insert_to_db(cur)
                response.pub = pubid
                response.valid.append(True)
                response.message.append(f"✔ Added Publication {pubid}.")

            except Exception as e:
                print(e)
                response.message.append(
                    f"✗  Publication Data is not correct. Error message: {e}"
                )
                pub = Publication()
                pubid = pub.insert_to_db(cur)
                response.valid.append(False)
            
            finally:
                try:
                    dataset_pub_q = """SELECT ts.insertdatasetpublication(%(datasetid)s, 
                                                                           %(publicationid)s, 
                                                                           %(primarypub)s)
                                    """
                    cur.execute(dataset_pub_q, {'datasetid': uploader["datasetid"].datasetid,
                                                'publicationid': pubid,
                                                'primarypub': True})
                except Exception as e:
                    print(e)
                    response.message.append("Could not associate dataset ID to publication ID")
                    response.valid.append(False)
                
        elif inputs['doi'][0] == 'TBD':
            response.message.append(f"No DOI present")
            response.valid.append(True)

        else:
            response.valid.append(False)
            response.message.append(f"✗  DOI is not properly formatted")
    else:
        response.message.append(f"No DOI present")
        response.valid.append(True)

    
    response.validAll = all(response.valid)
    return response


    

    