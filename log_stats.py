from collections import namedtuple
from typing import List
from pymongo.database import Database

SearchStat = namedtuple('SearchStat', ['keyword', 'count'])


class SearchAnalytics:
    """Processes search history statistics from MongoDB."""

    def __init__(self, db: Database) -> None:
        """
        Initializes the analytics engine with a MongoDB database.
        Args:
            db (Database): The active MongoDB database instance
        """
        self.db = db

    def get_popular_searches(self, limit: int = 5) -> List[SearchStat]:
        """
        Aggregates search history to find the most frequent search criteria.
        Args:
            limit (int): The number of top results to return. Defaults to 5.
        Returns:
            List[SearchStat]: A list of namedtuples containing the keyword and its frequency.
        """
        if self.db is None:
            return []

        try:
            pipeline = [
                {"$match": {"criteria": {"$exists": True}}},
                {"$group": {
                    "_id": {"$ifNull": ["$criteria.keyword", "$criteria.genre"]},
                    "count": {"$sum": 1}
                }},
                {"$sort": {"count": -1}},
                {"$limit": limit}
            ]
            results = list(self.db["search_history"].aggregate(pipeline))
            return [SearchStat(keyword=str(res["_id"]), count=res["count"]) for res in results]

        except Exception as e:
            return []