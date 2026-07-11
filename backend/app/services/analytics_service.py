from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import Student
from app.models.prediction import Prediction
from app.models.human_review import HumanReview
from app.core.constants import HIGH_RISK, MEDIUM_RISK, LOW_RISK, PENDING_REVIEW, APPROVED, REJECTED, MODIFIED
from app.schemas.analytics import AnalyticsOverview, RiskDistributionItem, RiskTrendItem, InterventionStatusOverview
from app.core.logging import logger

class AnalyticsService:
    @staticmethod
    async def get_overview(db: AsyncSession) -> AnalyticsOverview:
        try:
            # Total Students
            student_count_stmt = select(func.count(Student.id))
            student_count_result = await db.execute(student_count_stmt)
            total_students = student_count_result.scalar_one() or 0
            
            # Subquery for latest prediction per student
            latest_pred_subquery = (
                select(
                    Prediction.student_id,
                    func.max(Prediction.created_at).label("max_created_at")
                )
                .group_by(Prediction.student_id)
                .subquery()
            )
            
            # Get count per risk level for the latest predictions
            latest_preds_stmt = (
                select(Prediction.risk_level, func.count(Prediction.id))
                .join(
                    latest_pred_subquery,
                    (Prediction.student_id == latest_pred_subquery.c.student_id) &
                    (Prediction.created_at == latest_pred_subquery.c.max_created_at)
                )
                .group_by(Prediction.risk_level)
            )
            preds_res = await db.execute(latest_preds_stmt)
            pred_counts: dict[str, int] = {row[0]: row[1] for row in preds_res.all()}
            
            high_risk_count = pred_counts.get(HIGH_RISK, 0)
            medium_risk_count = pred_counts.get(MEDIUM_RISK, 0)
            low_risk_count = pred_counts.get(LOW_RISK, 0)
            
            # Pending reviews count
            pending_review_stmt = select(func.count(HumanReview.id)).where(HumanReview.status == PENDING_REVIEW)
            pending_res = await db.execute(pending_review_stmt)
            pending_reviews_count = pending_res.scalar_one() or 0
            
            return AnalyticsOverview(
                total_students=total_students,
                high_risk_count=high_risk_count,
                medium_risk_count=medium_risk_count,
                low_risk_count=low_risk_count,
                pending_reviews_count=pending_reviews_count
            )
        except Exception as e:
            logger.error(f"Error in get_overview: {str(e)}", exc_info=True)
            raise

    @staticmethod
    async def get_risk_distribution(db: AsyncSession) -> list[RiskDistributionItem]:
        try:
            # Subquery for latest prediction per student
            latest_pred_subquery = (
                select(
                    Prediction.student_id,
                    func.max(Prediction.created_at).label("max_created_at")
                )
                .group_by(Prediction.student_id)
                .subquery()
            )
            
            # Get count per risk level
            stmt = (
                select(Prediction.risk_level, func.count(Prediction.id))
                .join(
                    latest_pred_subquery,
                    (Prediction.student_id == latest_pred_subquery.c.student_id) &
                    (Prediction.created_at == latest_pred_subquery.c.max_created_at)
                )
                .group_by(Prediction.risk_level)
            )
            res = await db.execute(stmt)
            counts: dict[str, int] = {row[0]: row[1] for row in res.all()}
            
            total = sum(counts.values()) or 1 # avoid division by zero
            
            distribution = []
            for level in [LOW_RISK, MEDIUM_RISK, HIGH_RISK]:
                count = counts.get(level, 0)
                distribution.append(
                    RiskDistributionItem(
                        risk_level=level,
                        count=count,
                        percentage=round((count / total) * 100, 1)
                    )
                )
            return distribution
        except Exception as e:
            logger.error(f"Error in get_risk_distribution: {str(e)}", exc_info=True)
            raise

    @staticmethod
    async def get_risk_trends(db: AsyncSession) -> list[RiskTrendItem]:
        try:
            # Group all predictions by date and count risk levels
            # SQLite DATE(created_at) function gets the date string YYYY-MM-DD
            stmt = (
                select(
                    func.date(Prediction.created_at).label("pred_date"),
                    Prediction.risk_level,
                    func.count(Prediction.id)
                )
                .group_by(func.date(Prediction.created_at), Prediction.risk_level)
                .order_by("pred_date")
            )
            res = await db.execute(stmt)
            rows = res.all()
            
            # Format into structured list
            trends_by_date = {}
            for d_val, risk_level, count in rows:
                if not d_val:
                    continue
                # Ensure it is a string YYYY-MM-DD
                if not isinstance(d_val, str):
                    date_str = d_val.strftime("%Y-%m-%d")
                else:
                    date_str = d_val
                    
                if date_str not in trends_by_date:
                    trends_by_date[date_str] = {"high_risk": 0, "medium_risk": 0, "low_risk": 0}
                
                if risk_level == HIGH_RISK:
                    trends_by_date[date_str]["high_risk"] += count
                elif risk_level == MEDIUM_RISK:
                    trends_by_date[date_str]["medium_risk"] += count
                elif risk_level == LOW_RISK:
                    trends_by_date[date_str]["low_risk"] += count
                    
            # Fill missing intermediate dates if needed, or sort
            sorted_dates = sorted(trends_by_date.keys())
            
            trend_items = []
            for d in sorted_dates:
                trend_items.append(
                    RiskTrendItem(
                        date=d,
                        high_risk=trends_by_date[d]["high_risk"],
                        medium_risk=trends_by_date[d]["medium_risk"],
                        low_risk=trends_by_date[d]["low_risk"]
                    )
                )
                
            # Fallback empty list if database is empty
            if not trend_items:
                import datetime
                today = datetime.date.today().strftime("%Y-%m-%d")
                trend_items.append(RiskTrendItem(date=today, high_risk=0, medium_risk=0, low_risk=0))
                
            return trend_items
        except Exception as e:
            logger.error(f"Error in get_risk_trends: {str(e)}", exc_info=True)
            raise

    @staticmethod
    async def get_intervention_status(db: AsyncSession) -> InterventionStatusOverview:
        try:
            # Group reviews by status
            stmt = (
                select(HumanReview.status, func.count(HumanReview.id))
                .group_by(HumanReview.status)
            )
            res = await db.execute(stmt)
            counts: dict[str, int] = {row[0]: row[1] for row in res.all()}
            
            pending = counts.get(PENDING_REVIEW, 0)
            approved = counts.get(APPROVED, 0)
            rejected = counts.get(REJECTED, 0)
            modified = counts.get(MODIFIED, 0)
            
            reviewed_total = approved + rejected + modified
            approval_rate = round((approved / reviewed_total) * 100, 1) if reviewed_total > 0 else 0.0
            modification_rate = round((modified / reviewed_total) * 100, 1) if reviewed_total > 0 else 0.0
            
            return InterventionStatusOverview(
                pending=pending,
                approved=approved,
                rejected=rejected,
                modified=modified,
                approval_rate=approval_rate,
                modification_rate=modification_rate
            )
        except Exception as e:
            logger.error(f"Error in get_intervention_status: {str(e)}", exc_info=True)
            raise
