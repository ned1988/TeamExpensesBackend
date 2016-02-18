from flask_restplus import fields

from SharedModels import api


class Constants:
    def __init__(self):
        pass

    k_user = 'user'
    k_result = 'result'
    k_status = 'message'
    k_user_id = 'userID'
    k_event_id = 'eventID'
    k_is_removed = 'isRemoved'
    k_user_token = 'userToken'
    k_time_stamp = 'timeStamp'
    k_internal_id = 'internalID'
    k_team_members = 'teamMembers'
    k_user_details = 'userDetails'
    k_user_credentials_correct = 'user_credentials_correct'

    k_no_user_id = 'no_user_id'
    k_token_expired = 'token_expired'
    k_token_not_valid = 'token_not_valid'


    @staticmethod
    def error_login_response():
        error_login_response = api.model('ErrorLoginResponse', {
            Constants.k_status: fields.String(enum=[Constants.k_token_expired,
                                                    Constants.k_token_not_valid,
                                                    Constants.k_no_user_id])
        })

        return error_login_response

    @staticmethod
    def error_token_not_valid():
        return {Constants.k_status: 'token_not_valid'}, 401

    @staticmethod
    def error_token_expired():
        return {Constants.k_status: 'token_expired'}, 401

    @staticmethod
    def error_no_user_id():
        return {Constants.k_status: 'no_user_id'}, 401

    @staticmethod
    def error_wrong_json_format():
        return {Constants.k_status: 'wrong_json_not_valid'}, 401

    @staticmethod
    def error_wrong_json_structure():
        return {Constants.k_status: 'wrong_json_structure'}, 401

    @staticmethod
    def error_missed_parameter(parameter):
        return {Constants.k_status: 'missed_parameter ' + parameter}, 401

    @staticmethod
    def error_with_message_and_status(message, status):
        return {Constants.k_status: message}, status
