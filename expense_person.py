from datetime import datetime

from SharedModels import db
from constants import Constants
from PersonModel import PersonModel
from expense_model import ExpenseModel


class ExpensePerson(db.Model):
    __tablename__ = 'expense_person'

    k_expense_person_id = 'expensePersonID'

    expense_person_id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense_model.expense_id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person_model.person_id'))
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    @classmethod
    def find_rows_for_user(cls, user_id):
        """Find all expenses with current user
        :param user_id: User ID
        :return:List of ExpensePerson objects
        """
        if user_id is None or not isinstance(user_id, int):
            return []

        rows = ExpensePerson.query.filter_by(person_id=user_id).all()

        return rows

    @classmethod
    def find_rows_for_user_time_stamp(cls, user_id, time_stamp):
        """
        Search all rows with current user_id value which are greater than time_stamp value
        :param user_id:
        :param time_stamp:
        :return:
        """
        if time_stamp is None:
            items = ExpensePerson.find_rows_for_user(user_id)
        else:
            items = ExpensePerson.query.filter(ExpensePerson.person_id == user_id,
                                               ExpensePerson.time_stamp > time_stamp).all()

        return items

    @classmethod
    def find_expense_person(cls, expense_person_id):
        items = ExpensePerson.query.filter_by(expense_person_id=expense_person_id).all()

        if len(items) > 0:
            return items[0]
        else:
           return None

    def init_object(self):
        self.is_removed = False

    def configure_with_dict(self, dict_model):
        value = dict_model.get(ExpenseModel.k_expense_id)
        if value is not None:
            self.expense_id = value

        value = dict_model.get(PersonModel.k_person_id)
        if value is not None:
            self.person_id = value

        value = dict_model.get(Constants.k_is_removed)
        if value is not None:
            self.is_removed = value

        # Update time stamp each time we update model from user
        self.time_stamp = datetime.utcnow()

    def to_dict(self):
        json_object = dict()

        json_object[ExpensePerson.k_expense_person_id] = self.expense_person_id
        json_object[ExpenseModel.k_expense_id] = self.expense_id
        json_object[PersonModel.k_person_id] = self.person_id
        json_object[Constants.k_is_removed] = self.is_removed

        return json_object
