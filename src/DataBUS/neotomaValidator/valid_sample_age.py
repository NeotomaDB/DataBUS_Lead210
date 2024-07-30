import DataBUS.neotomaHelpers as nh
from DataBUS import SampleAge, Response


def valid_sample_age(cur, yml_dict, csv_file, validator):
    """
    Inserts sample age data into a database.

    Args:
        cur (cursor object): Database cursor to execute SQL queries.
        yml_dict (dict): Dictionary containing YAML data.
        csv_file (str): File path to the CSV template.
        uploader (dict): Dictionary containing uploader details.

    Returns:
        response (dict): A dictionary containing information about the inserted sample ages.
            - 'sampleAge' (list): List of IDs for the inserted sample age data.
            - 'valid' (bool): Indicates if all insertions were successful.
    """
    response = Response()

    params = ["age"]
    inputs = nh.pull_params(params, yml_dict, csv_file, "ndb.sampleages")

    # inputs['age'] = [float(value) if value != 'NA' else None for value in inputs['age']]
    inputs["uncertainty"] = [
        float(value) if value != "NA" else None for value in inputs["uncertainty"]
    ]

    for i in range(0, validator["sample"].sa_counter):
        if isinstance(inputs["age"][i], (int, float)):
            age_younger = inputs["age"][i] - inputs["uncertainty"][i]
            age_older = inputs["age"][i] + inputs["uncertainty"][i]
        else:
            response.message.append(
                "? Age is set to None. Ageyounger/Ageolder will be None."
            )
            age_younger = None
            age_older = None
        try:
            sa = SampleAge(
                sampleid=2,  # Placeholder
                chronologyid=2,  # Placeholder
                age=inputs["age"][i],
                ageyounger=age_younger,
                ageolder=age_older,
            )
            response.valid.append(True)
            response.message.append(f"✔ Sample ages can be created.")
        except Exception as e:
            response.valid.append(False)
            response.message.append(f"✗ Samples ages cannot be created. {e}")

    response.valid = all(response.valid)
    return response
