# Utility modules
# Author: Indrajit Ghosh
# Created On: Nov 22, 2023

from datetime import datetime, timezone

def convert_to_iso8601_utc(input_date_str):
    """
    Convert date string from "Nov 22, 2023 04:31:32 PM IST" to "2023-11-22T11:01:32.541098+00:00".

    Parameters:
    - input_date_str (str): Input date string in the format "Mmm DD, YYYY HH:mm:ss AM/PM TZ".

    Returns:
    - str: Converted date string in the format "YYYY-MM-DDTHH:mm:ss.microseconds+00:00".
    """

    # Define the input and output date formats
    input_format = "%b %d, %Y %I:%M:%S %p %Z"
    output_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    # Parse the input date string
    input_date = datetime.strptime(input_date_str, input_format)

    # Convert to UTC and format the output date string
    output_date_str = input_date.astimezone(timezone.utc).strftime(output_format)

    # Ensure the UTC offset has a colon in the format "+00:00"
    output_date_str = output_date_str[:-2] + ":" + output_date_str[-2:]

    return output_date_str



def main():
    # Example usage
    input_date_str = "Nov 22, 2023 04:31:32 PM IST"
    output_date_str = convert_to_iso8601_utc(input_date_str)
    print(output_date_str)


if __name__ == '__main__':
    main()
    
