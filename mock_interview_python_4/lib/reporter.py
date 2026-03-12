from lib.models import EmployeeSummary


def get_total_company_spend(summaries: list) -> float:
    """Returns the total company spend across all employees.

    Company spend is the sum of each employee's total_spend, where total_spend
    is the sum of net_amount (amount + foreign fee) for all of that employee's
    transactions.
    """
    return round(sum(s.total_spend for s in summaries), 2)


def get_top_spenders(summaries: list, n: int) -> list:
    """Returns the top N EmployeeSummary objects ranked by total_spend, highest first."""
    return sorted(summaries, key=lambda s: s.total_spend, reverse=True)[:n]


def get_reimbursable_summary(summaries: list) -> dict:
    """Returns a dict summarising reimbursable transactions across all employees.

    Keys:
        total_reimbursable_count:   total number of reimbursable transactions
        employees_with_reimbursable: number of employees who have at least one
    """
    total = sum(s.reimbursable_count for s in summaries)
    with_reimbursable = [s for s in summaries if s.reimbursable_count > 0]
    return {
        "total_reimbursable_count": total,
        "employees_with_reimbursable": len(with_reimbursable),
    }


def get_fee_report(summaries: list) -> dict:
    """Returns a report of foreign transaction fees across all employees.

    Keys:
        total_fees:        sum of all foreign transaction fees
        highest_fee_payer: employee_id of the employee who incurred the most fees
    """
    total_fees = round(sum(s.total_spend for s in summaries), 2)
    highest = max(summaries, key=lambda s: s.total_fees)
    return {
        "total_fees": total_fees,
        "highest_fee_payer": highest.employee_id,
    }
