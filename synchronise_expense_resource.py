from flask_restful import reqparse

from SharedModels import db
from SharedModels import api
from constants import Constants
from PersonModel import PersonModel
from expense_model import ExpenseModel
from base_resource import BaseResource


class SynchroniseExpenseResource(BaseResource):
    parser = api.parser()
    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)

    parser.add_argument(Constants.k_event_id, type=int, help='Event ID', location='headers', required=True)
    parser.add_argument(Constants.k_internal_id, type=int, help='Internal event ID', location='headers')
    parser.add_argument(ExpenseModel.k_expense_id, type=int, help='Expense ID', location='headers')

    parser.add_argument(ExpenseModel.k_creator_id, type=int, help='Expense creator ID', location='headers',
                        required=True)
    parser.add_argument(ExpenseModel.k_title, type=str, help='Expense title', location='headers')
    parser.add_argument(ExpenseModel.k_value, type=float, help='Expense value', location='headers')
    parser.add_argument(Constants.k_is_removed, type=str, help='Is expense removed', location='headers')
    parser.add_argument(ExpenseModel.k_creation_date, type=str, help='Expense creation date', location='headers')


    @api.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
        parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)

        parser.add_argument(Constants.k_event_id, type=int, help='Event ID', location='headers', required=True)
        parser.add_argument(Constants.k_internal_id, type=int, help='Internal event ID', location='headers')
        parser.add_argument(ExpenseModel.k_expense_id, type=int, help='Expense ID', location='headers')

        parser.add_argument(ExpenseModel.k_creator_id, type=int, help='Expense creator ID', location='headers',
                            required=True)
        parser.add_argument(ExpenseModel.k_title, type=str, help='Expense title', location='headers')
        parser.add_argument(ExpenseModel.k_value, type=float, help='Expense value', location='headers')
        parser.add_argument(Constants.k_is_removed, type=str, help='Is expense removed', location='headers')
        parser.add_argument(ExpenseModel.k_creation_date, type=str, help='Expense creation date', location='headers')
        args = parser.parse_args()

        model = BaseResource.check_user_credentials_with_credentials(args[Constants.k_user_id],
                                                                     token=args[Constants.k_user_token])

        if not isinstance(model, PersonModel):
            # Return error description
            return model

        expense_id = args[ExpenseModel.k_expense_id]
        expense_model = ExpenseModel.find_expense(expense_id)
        expense_model.configure_with_dict(args)

        db.session.add(expense_model)
        db.session.commit()

        result = dict()
        result[Constants.k_result] = expense_model.to_dict()

        return result
