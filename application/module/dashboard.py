from datetime import datetime, timedelta

from sqlalchemy import func

from . import *


class DashboardModel:

    @classmethod
    def news_feed(cls):
        _user: User = User.query.filter_by(id=current_user.id).first()
        if not _user:
            raise CustomException(message="User not found")
        _parents: List[Student] = _user.parents.students if _user.parents else None
        _teachers: Teacher = _user.teachers if _user.teachers else None

        groups = []

        if _parents:
            groups: List[LearningGroup] = [x.learning_groups for x in _parents]

        if _teachers:
            groups: List[LearningGroup] = [x for x in _teachers.learning_groups]

        if groups:

            all_learning_groups = [group for sublist in groups for group in sublist] if _parents else groups

            comments = []
            files = []
            if all_learning_groups:
                for l_groups in all_learning_groups:
                    comments.extend([
                        {
                            **x.to_dict(add_filter=False),
                            "commented_by": {
                                **x.user.to_dict(),
                                **User.GetUserObject(x.user.id)
                            },
                        }
                        for x in l_groups.learning_group_comments])

                    files.extend([
                        {
                            **x.to_dict(add_filter=False),
                            "uploaded_by": {'email': x.user.email, **User.GetUserObject(x.user.id)},
                            "file_url": FileHandler.get_file_url(x.file_path)

                        }
                        for x in l_groups.learning_group_files])

                return {'comments': comments, 'files': files}
            else:
                return "No groups found"
        else:
            return "No groups found"

    @classmethod
    def school_stat(cls):
        return {
            "total_schools": School.query.count(),
            "total_teachers": Teacher.query.count(),
            "total_students": Student.query.count(),
        }

    @classmethod
    def get_monthly_statistics(cls, year):
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

        monthly_stats = {month: {'active': 0, 'processing': 0, 'cancelled': 0} for month in months}

        # Fetch data with a single query for better performance
        result = db.session.query(
            func.extract('month', func.to_timestamp(Subscription.created_at)).label('month'),
            Subscription.status,
            func.count().label('count')
        ).filter(
            func.extract('year', func.to_timestamp(Subscription.created_at)) == year
        ).group_by(func.extract('month', func.to_timestamp(Subscription.created_at)), Subscription.status).all()

        # Aggregate the counts into the result dictionary
        for row in result:
            month = row[0]
            status = row[1]
            count = row[2]
            month_name = months[int(month - 1)]
            monthly_stats[month_name][status.value] = count

        return monthly_stats

    @classmethod
    def activity_feed(cls):
        _audit = Audit.query.order_by(desc(Audit.created_at)).limit(5).all()
        return [{
            "image": x.user.admins.profile_image or None,
            "action": x.action,
            "created_at": x.created_at,
            "action_performed_by": f"{x.user.admins.first_name} {x.user.admins.last_name}" if x.user.admins else x.user.managers.name
        } for x in _audit]

    def filter_revenue_by_month(month: int, year: int):
        first_day_of_month = datetime.datetime(year, month, 1)
        last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        # Calculate the number of weeks in the month
        weeks = ((last_day_of_month - first_day_of_month).days // 7)

        # Calculate revenue per week
        weekly_revenue = {}
        for i in range(weeks):
            start_date = first_day_of_month + timedelta(7 * i)
            end_date = start_date + timedelta(days=6)

            weekly_total = (
                    db.session.query(func.sum(Transaction.amount))
                    .filter(Transaction.completed_at >= start_date, Transaction.completed_at <= end_date)
                    .scalar() or 0
            )
            weekly_revenue[f'Week {i + 1}'] = weekly_total

        # Calculate total revenue for the month
        total_revenue = (
                db.session.query(func.sum(Transaction.amount))
                .filter(Transaction.completed_at >= first_day_of_month, Transaction.completed_at <= last_day_of_month)
                .scalar() or 0
        )
        return {
            "weeks": weekly_revenue,
            "total_month_revenue": total_revenue
        }

    @classmethod
    def recently_added_school(cls):
        _school = School.query.order_by(desc(School.created_at)).limit(3).all()
        return [{
            **x.to_dict(add_filter=False)
        } for x in _school]
