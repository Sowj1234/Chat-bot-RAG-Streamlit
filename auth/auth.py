from auth.employee_db import EmployeeDB


class AuthManager:

    def __init__(self):
        self.employee_db = EmployeeDB()

    def login(self, employee_id, employee_name):
        """
        Authenticate an employee.

        Returns:
            (True, user_dict)  -> if authentication succeeds
            (False, error_msg) -> otherwise
        """

        return self.employee_db.get_employee(employee_id, employee_name)