CREATE OR REPLACE FUNCTION insert_data_uncertainty(_dataid numeric,
                                                   _uncertaintyvalue numeric DEFAULT NULL::numeric,
                                                   _uncertaintyunitid numeric DEFAULT NULL::numeric,
                                                   _uncertaintybasisid numeric DEFAULT NULL::numeric,
                                                   _notes character varying DEFAULT NULL::character varying)
RETURNS void
LANGUAGE sql
AS $function$
insert into ndb.datauncertainties (dataid, uncertaintyvalue, uncertaintyunitid, uncertaintybasisid, notes)
values (_dataid,
        _uncertaintyvalue,
        _uncertaintyunitid,
        _uncertaintybasisid,
        _notes)
$function$