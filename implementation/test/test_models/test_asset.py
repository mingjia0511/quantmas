"""Tests for Asset model."""
from src.models.asset import Asset


class TestAsset:
    """Test suite for Asset model."""

    def test_asset_creation(self) -> None:
        """Should create asset with all attributes."""
        asset = Asset(
            id="asset_1",
            name="Snowflake Manor",
            asset_type="Real Estate",
            sub_type="Residential",
            available_on_day=1,
            region="Frostpeak",
        )

        assert asset.id == "asset_1"
        assert asset.name == "Snowflake Manor"
        assert asset.available_on_day == 1

    def test_asset_is_available_before_day(self) -> None:
        """Should return False when day is before available_on_day."""
        asset = Asset(
            id="asset_3",
            name="Test",
            asset_type="Real Estate",
            sub_type="Residential",
            available_on_day=45,
            region="Test",
        )

        assert not asset.is_available(44)

    def test_asset_is_available_on_exact_day(self) -> None:
        """Should return True on exact available_on_day."""
        asset = Asset(
            id="asset_3",
            name="Test",
            asset_type="Real Estate",
            sub_type="Residential",
            available_on_day=45,
            region="Test",
        )

        assert asset.is_available(45)

    def test_asset_is_available_after_day(self) -> None:
        """Should return True after available_on_day."""
        asset = Asset(
            id="asset_3",
            name="Test",
            asset_type="Real Estate",
            sub_type="Residential",
            available_on_day=45,
            region="Test",
        )

        assert asset.is_available(46)
        assert asset.is_available(100)

    def test_asset_is_immutable(self) -> None:
        """Should not allow modification of attributes."""
        asset = Asset(
            id="asset_1",
            name="Test",
            asset_type="Real Estate",
            sub_type="Residential",
            available_on_day=1,
            region="Test",
        )

        try:
            asset.id = "asset_2"  # type: ignore
            assert False, "Should not allow modification"
        except AttributeError:
            pass  # Expected
