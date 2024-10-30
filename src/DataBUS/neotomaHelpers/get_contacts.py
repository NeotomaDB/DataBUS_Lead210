def get_contacts(cur, contacts_list):
    get_contact = (
        """SELECT contactid, contactname, similarity(contactname, %(name)s) AS sim_score
                    FROM ndb.contacts
                    WHERE contactname %% %(name)s
                    ORDER BY sim_score DESC
                    LIMIT 3;"""
    )
    baseid = 1
    contids = list()
    for i in contacts_list:
        cur.execute(get_contact, {"name": i})
        data = cur.fetchone()
        d_name = data[1]
        d_id = data[0]
        result = d_name.startswith(i.rstrip("."))
        if result == True:
            contids.append({"name": d_name, "id": d_id, "order": baseid})
        else:
            contids.append({"name": i, "id": None, "order": baseid})
        baseid +=1
    
    return contids
