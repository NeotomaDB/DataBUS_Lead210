import pandas as pd
import os

"""
To run from command line use:
python csv_validator.py /path/to/directory
Example:/
python 210Pb_Template/neotomaUploader/csvValidator.py --path=210Pb_Template/data/ --template=210Pb_Template/template.yml
"""


def valid_csv(filename, yml_data):
    """_Validate csv file for use in the validator._

    Args:
        filename (_string_): _A valid csv filename._
        yml_data (_dict_): _A dict passed from template_to_dict()_

    Returns:
        _type_: _description_
    """
    response = {"valid": [], "message": []}
    # response = []
    # Take directly from .yml file
    col_values = [d.get("column") for d in yml_data]
    # Remove specific columns from col_values as they are taken from the metadata in the xlsx template
    columns_to_remove = ["databaseid", "databasename", "datasettypeid", "labnumber", "variableelement"]
    col_values = [col for col in col_values if col not in columns_to_remove]

    if not os.path.isfile(filename):
        raise FileNotFoundError(
            f"The file '{filename}' could not be found within the current path."
        )

    try:
        # Load csv file as data frame and extract columns
        df = pd.read_csv(filename)
    except pd.errors.ParserError:
        response["message"].append(f"✗  Error opening file '{filename}': {e}" + "\n")

    df_columns = list(df.columns)
    # Verify that all columns from the DF are in the YAML file
    diff_col = sorted(set(col_values) - set(df_columns))

    # Verify that all columns from the YAML are in the DF
    diff_val = sorted(set(df_columns) - set(col_values))

    # Report in the log
    if diff_col == diff_val:
        response["message"].append("✔  The column names and flattened YAML keys match")
        response["valid"].append(True)
    else:
        response["message"].append(
            "?  The column names and flattened YAML keys do not match"
        )
        response["message"].append(
            f"Columns from the data frame not in the YAML template: {diff_val}"
        )
        response["message"].append(
            f"Columns from the YAML template are not in the data frame: {diff_col}"
        )
        response["valid"].append(False)
    response["valid"] = all(response["valid"])
    return response
