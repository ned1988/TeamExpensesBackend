from flask_restful import reqparse

from SharedModels import db
from SharedModels import api
from constants import Constants
from PersonModel import PersonModel
from base_resource import BaseResource
from expense_model import ExpenseModel
from expense_person import ExpensePerson


class SynchroniseExpensePersonResource(BaseResource):
    parser = api.parser()
    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    # parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)

    parser.add_argument(ExpenseModel.k_expense_id, type=int, help='Expense ID', location='headers', required=True)
    parser.add_argument(PersonModel.k_person_id, type=int, help='Person ID', location='headers', required=True)
    parser.add_argument(ExpensePerson.k_expense_person_id, type=int, help='Expense Person ID', location='headers')
    parser.add_argument(Constants.k_is_removed, type=str, help='Is team member removed from event', location='headers')

    @api.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
        # parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)

        parser.add_argument(ExpenseModel.k_expense_id, type=int, help='Expense ID', location='headers', required=True)
        parser.add_argument(PersonModel.k_person_id, type=int, help='Person ID', location='headers', required=True)
        parser.add_argument(ExpensePerson.k_expense_person_id, type=int, help='Expense Person ID', location='headers')
        parser.add_argument(Constants.k_is_removed, type=str, help='Is team member removed from event',
                            location='headers')
        args = parser.parse_args()

        user_id = args[Constants.k_user_id]
        # token = args[Constants.k_user_token]
        # current_user = BaseResource.check_user_credentials_with_credentials(user_id, token=token)
        #
        # if not isinstance(current_user, PersonModel):
        #     # Return error description
        #     return current_user

        expense_person_id = args[ExpensePerson.k_expense_person_id]
        expense_person = ExpensePerson.find_expense_person(expense_person_id)
        if expense_person is None:
            expense_person = ExpensePerson()
            expense_person.init_object()

        expense_person.configure_with_dict(args)

        db.session.add(expense_person)
        db.session.commit()

        result = dict()
        result[Constants.k_result] = expense_person.to_dict()

        return result
