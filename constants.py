class Constants:
    def __init__(self):
        pass

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
        return {'status': 'wrong_json_format'}, 401

    @staticmethod
    def error_wrong_json_structure():
        return {'status': 'wrong_json_structure'}, 401
