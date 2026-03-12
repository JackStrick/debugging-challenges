class Transaction:
    """A raw expense transaction as loaded from the data source."""

    def __init__(
        self,
        id: int,
        employee_id: str,
        amount: float,
        currency: str,
        category: str,
        status: str,
    ):
        self.id = id
        self.employee_id = employee_id
        self.amount = amount
        self.currency = currency
        self.category = category
        self.status = status


class ProcessedTransaction:
    """A Transaction after fee calculation and reimbursability determination.

    Attributes:
        transaction:      the original Transaction object
        fee:              foreign transaction fee (0.0 for USD transactions)
        net_amount:       total cost to the company — the transaction amount plus
                          any applicable foreign fee
        is_reimbursable:  True if the transaction is eligible for reimbursement
    """

    def __init__(self, transaction: Transaction, fee: float, is_reimbursable: bool):
        self.transaction = transaction
        self.fee = fee
        self.net_amount = transaction.amount - fee
        self.is_reimbursable = is_reimbursable


class EmployeeSummary:
    """Aggregated spend metrics for a single employee.

    Attributes:
        employee_id:        the employee's identifier
        processed:          list of ProcessedTransactions belonging to this employee
        total_spend:        sum of net_amount across all of the employee's transactions
        total_fees:         sum of foreign fees across all of the employee's transactions
        reimbursable_count: number of transactions eligible for reimbursement
    """

    def __init__(self, employee_id: str, processed: list):
        self.employee_id = employee_id
        self.processed = processed
        self.total_spend = round(sum(p.net_amount for p in processed), 2)
        self.total_fees = round(sum(p.fee for p in processed), 2)
        self.reimbursable_count = sum(1 for p in processed if p.is_reimbursable)
