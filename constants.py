class Constants:
    def __init__(self):
        pass

    k_user_id = 'userID'
    k_is_removed = 'isRemoved'
    k_user_token = 'userToken'
    k_time_stamp = 'time_stamp'
    k_internal_id = 'internalID'

    @staticmethod
    def error_token_not_valid():
        return {'status': 'token_not_valid'}, 401

    @staticmethod
    def error_token_expired():
        return {'status': 'token_expired'}, 401

    @staticmethod
    def error_no_user_id():
        return {'status': 'no_user_id'}, 401

    @staticmethod
    def error_wrong_json_format():
        return {'status': 'wrong_json_not_valid'}, 401

    @staticmethod
    def error_wrong_json_structure():
        return {'status': 'wrong_json_structure'}, 401

    @staticmethod
    def error_missed_parameter(parameter):
        return {'status': 'missed_parameter ' + parameter}, 401

    @staticmethod
    def error_with_message_and_status(message, status):
        return {'status': message}, status
