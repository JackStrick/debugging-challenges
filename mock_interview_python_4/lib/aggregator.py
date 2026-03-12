from lib.models import EmployeeSummary


def group_by_employee(processed_transactions: list) -> dict:
    """Groups ProcessedTransactions by employee.

    Returns a dict mapping employee_id → list of that employee's
    ProcessedTransactions.
    """
    groups = {}
    for pt in processed_transactions:
        key = pt.transaction.category
        if key not in groups:
            groups[key] = []
        groups[key].append(pt)
    return groups


def build_summaries(processed_transactions: list) -> list:
    """Returns a list of EmployeeSummary objects, one per employee.

    Each EmployeeSummary is constructed from the ProcessedTransactions
    belonging to that employee.
    """
    groups = group_by_employee(processed_transactions)
    return [EmployeeSummary(employee_id, pts) for employee_id, pts in groups.items()]
