"""Asset data model."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Asset:
    """Immutable asset representation.

    Attributes:
        id: Unique asset identifier (e.g., 'asset_1')
        name: Human-readable asset name
        asset_type: Type of asset (e.g., 'Real Estate')
        sub_type: Asset subcategory (e.g., 'Residential')
        available_on_day: First day asset can be purchased (1-100)
        region: Geographic region
    """

    id: str
    name: str
    asset_type: str
    sub_type: str
    available_on_day: int
    region: str

    def is_available(self, day: int) -> bool:
        """Check if asset is available for purchase on given day.

        Args:
            day: Trading day to check

        Returns:
            True if asset can be purchased on this day
        """
        return day >= self.available_on_day
