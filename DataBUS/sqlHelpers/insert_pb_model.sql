CREATE OR REPLACE FUNCTION insert_lead_model(_pbbasisid numeric,
                                            _analysisunitid numeric, 
                                            _cumulativeinventory numeric)
RETURNS void
LANGUAGE sql
AS $function$
insert into ndb.leadmodels (pbbasisid, analysisunitid, cumulativeinventory)
values (_pbbasisid,
        _analysisunitid,
        _cumulativeinventory)
$function$