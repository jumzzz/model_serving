from utils import load_json


class StandardPayload:
    """Class object for validating if the payload is a standard json payload. 
       It checks for various error such as Missing Fields, Invalid Data types, 
       Proper Categorical Data, and Negative Values.
    """

    def __init__(self, ref_json : str):
        self.standard_payload = load_json(ref_json)


    def wrap_data(self, data) -> dict:
        """Initially wraps the raw payload to proper
           dict format
        Args:
            data : Raw json payload

        Returns:
            dict: wrapped json payload
        """
  
        return {
            'has_error' : False,
            'data' : data
        }

    def lower_case(self, data : dict) -> dict:
        """Apply lowercasing to all string-typed fields

        Args:
            data (dict): Wrapped json payload

        Returns:
            dict: Payload with lower-cased strings
        """
        for k,v in data['data'].items():
            if type(v) is str:
                data['data'][k] = v.lower()
            else:
                data['data'][k] = v
        return data

    def fill_optional_fields(self, data : dict) -> dict:
        """If an optional field was missing in the payload,
           it will create an entry of that field an set 
           the value to \"?\"

        Args:
            data (dict): Wrapped json payload

        Returns:
            dict: Payload filled with optional-fields
        """
        for field in self.standard_payload['optional_fields']:
            if field not in data['data']:
                data['data'][field] = '?'
        return data

    
    def update_if_error_exist(self, data : dict, 
                                    error_list : list, 
                                    error_type : str) -> dict:
        """Modifies the payload if a particular error was detected

        Args:
            data (dict): Wrapped json payload
            error_list (list): list of errors found
            error_type (str): Type of error

        Returns:
            dict: Wrapped Payload that contains error information
        """

        if len(error_list) > 0:
            data['has_error'] = True
            data['error_msg'] = {
                'status' : 'error',
                'error_type' : error_type,
                 error_type : error_list
            }
        return data

    def check_missing_fields(self, data : dict) -> dict:
        """Modifies the payload if missing fields are detected.

        Args:
            data (dict): Wrapped json payload

        Returns:
            dict: Contains missing fields if there are any
        """
        missing = []

        for field in self.standard_payload['mandatory_fields']:
            if field not in data['data']:
                missing.append(field)

        data = self.update_if_error_exist(data, 
                                          missing, 
                                          'missing_fields')
        return data

    def remove_excess_field(self, data: dict) -> dict:
        """Remove unnecessary fields

        Args:
            data (dict): Wrapped json payload

        Returns:
            dict: Payload pruned with unnecessary fields
        """
        data_ref = data['data'].copy()

        data['data'] = {k : data_ref[k] for k in self.standard_payload['mandatory_fields']}
        return data


    def check_data_types(self, data : dict) -> dict:
        """Modifies the payload if there are mistyped fields.

        Args:
            data (dict): Wrapped json payload

        Returns:
            dict: Contains mistyped fields if there are any
        """

        invalid_types = []

        for k, v in self.standard_payload['proper_types'].items():
            data_type = str(type(data['data'][k]))
   
            if data_type != v:
                invalid_types.append(k)

        data = self.update_if_error_exist(data, 
                                          invalid_types,
                                          'invalid_data_type')

        return data

    def check_categorical_data(self, data : dict) -> dict:
        """Modifies the payload if there are invalid values for categorical fields

        Args:
            data (dict): Wrapped json payload

        Returns:
            dict: Contains the categorical fields with invalid values if there are any
        """

        invalid_categories = []

        for field, cat_allowed in self.standard_payload['categorical_data'].items():
            input_cat = data['data'][field]

            if input_cat not in cat_allowed:
                invalid_categories.append(field)

        data = self.update_if_error_exist(data, invalid_categories, 'invalid_categorical_data')
        return data

    
    def check_negative_data(self, data: dict) -> dict:
        """Modfies the payload if there are negative values for numerical fields

        Args:
            data (dict): Wrapped json payload

        Returns:
            dict: Contains the numerical fields with negative values if there are any
        """

        with_negative_values = []

        for field in self.standard_payload['numerical_data']:
            if data['data'][field] < 0:
                with_negative_values.append(field)

        data = self.update_if_error_exist(data, with_negative_values, 'fields_with_negative')
        return data


    def valid_json(self, data : dict) -> dict:
        """Check if data is a valid json

        Args:
            data (dict): Wrapped Payload

        Returns:
            dict: Contains an indication that the data is empty or None.
        """

        error_list = []

        if type(data['data']) is not dict:
            error_list.append('payload is not a json')
            data = self.update_if_error_exist(data, error_list, 'invalid_json')
        else:
            if len(data['data']) == 0:
                error_list.append('empty json')
                data = self.update_if_error_exist(data, error_list, 'invalid_json')
    
        return data


    def validate_data(self, data) -> dict:
        """Runs the payload validation end to end

        Args:
            data: Raw json payload

        Returns:
            dict: Wrapped json payload. Contains error information if there are any
        """

        data = self.wrap_data(data)
        data = self.valid_json(data)
        if data['has_error']: return data

        data = self.lower_case(data)
        data = self.fill_optional_fields(data)
        
        data = self.check_missing_fields(data)
        if data['has_error']: return data

        data = self.remove_excess_field(data)
        data = self.check_data_types(data)
        if data['has_error']: return data

        data = self.check_categorical_data(data)
        if data['has_error']: return data

        data = self.check_negative_data(data)
        return data
