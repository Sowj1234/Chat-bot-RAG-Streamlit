from pathlib import Path
import pandas as pd


class EmployeeDB:

    def __init__(self, file_path=None):

        if file_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            file_path = base_dir / "data" / "HR" / "hr_data.csv"

        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)

        # Remove leading/trailing spaces from column names
        self.df.columns = self.df.columns.str.strip()

    def get_employee(self, employee_id, employee_name):
        """
        Returns employee details if found.
        Otherwise returns None.
        """

        employee_id = str(employee_id).strip()
        employee_name = employee_name.strip().lower()

        employee = self.df[
            (self.df["employee_id"].astype(str).str.strip() == employee_id)
            &
            (self.df["full_name"].str.strip().str.lower() == employee_name)
        ]

        if employee.empty:
            return None

        row = employee.iloc[0]

        return {
            "employee_id": row["employee_id"],
            "name": row["full_name"],
            "role": row["role"],
            "department": row["domain"]
        }