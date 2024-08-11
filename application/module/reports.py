from collections import defaultdict
from datetime import datetime

from sqlalchemy import func

from application import *
from application.models.subscription import SubscriptionStatusEnum, Subscription
from application.models.transactions import Transaction


class ReportModel:

    @classmethod
    def revenues(cls):
        # Assuming SubscriptionStatusEnum has an 'ACTIVE' value defined
        active_status_value = SubscriptionStatusEnum.ACTIVE.value
        # Query to calculate total subscription revenue
        total_subscription_revenue = db.session.query(func.sum(Subscription.amount)).filter(Subscription.status == active_status_value).scalar()
        total_transaction_revenue = db.session.query(func.sum(Transaction.amount)).filter(Transaction.status == "success").scalar()

        return {
            "subscription_revenue": total_subscription_revenue,
            "transaction_revenue": total_transaction_revenue,
            "total_revenue": total_subscription_revenue + total_transaction_revenue
        }

    @classmethod
    def subscription_transaction(cls):
        active_status_value = SubscriptionStatusEnum.ACTIVE.value

        total_subscription_revenue = db.session.query(func.sum(Subscription.amount)).filter(Subscription.status == active_status_value).scalar()
        total_transaction_revenue = db.session.query(func.sum(Transaction.amount)).filter(Transaction.status == "success").scalar()
        total_revenue = total_subscription_revenue + total_transaction_revenue
        return {
            "subscription_revenue_percentage": (total_subscription_revenue / total_revenue) * 100,
            "transaction_revenue_percentage": (total_transaction_revenue / total_revenue) * 100,
        }

    @classmethod
    def revenue_breakdown(cls):
        # Calculate total subscription revenue per quarter for each year
        subscription_revenue_breakdown = db.session.query(
            func.extract('year', func.to_timestamp(Subscription.created_at)).label('year'),
            func.extract('quarter', func.to_timestamp(Subscription.created_at)).label('quarter'),
            func.sum(Subscription.amount).label('total_revenue')
        ).group_by('year', 'quarter').all()

        # Calculate total transaction revenue per quarter for each year
        transaction_revenue_breakdown = db.session.query(
            func.extract('year', Transaction.completed_at).label('year'),
            func.extract('quarter', Transaction.completed_at).label('quarter'),
            func.sum(Transaction.amount).label('total_revenue')
        ).filter(Transaction.status == 'success').group_by('year', 'quarter').all()

        # Combine the two revenue breakdowns
        combined_revenue_breakdown = defaultdict(lambda: defaultdict(float))

        for item in subscription_revenue_breakdown + transaction_revenue_breakdown:
            year = int(item.year)
            quarter = int(item.quarter)
            total_revenue = float(item.total_revenue)

            combined_revenue_breakdown[year][quarter] += total_revenue

        # Create the final result dictionary with missing quarters filled in with 0
        final_result = {}
        for year, quarters_data in combined_revenue_breakdown.items():
            final_result[year] = {
                i: quarters_data.get(i, 0) for i in range(1, 5)
            }

        return {'result': final_result}

    @classmethod
    def revenue_analytics(cls, year):
        revenue_analytics = {}

        # Loop through each month from January to December
        for month in range(1, 13):
            # Calculate total revenue for the specific month and year
            total_revenue = db.session.query(
                func.sum(Subscription.amount)  # Replace with your revenue calculation query
            ).filter(
                func.extract('year', func.to_timestamp(Subscription.created_at)) == year,
                func.extract('month', func.to_timestamp(Subscription.created_at)) == month
            ).scalar() or 0.0  # If no revenue found, set to 0.0

            # Store revenue in the analytics dictionary for the corresponding month
            revenue_analytics[datetime(year, month, 1).strftime('%B')] = total_revenue

        return revenue_analytics


