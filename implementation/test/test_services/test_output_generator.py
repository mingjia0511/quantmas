"""Tests for OutputGenerator service."""
import yaml
from pathlib import Path
from src.services.output_generator import OutputGenerator
from src.strategies.buy_and_hold_strategy import Trade


class TestOutputGenerator:
    """Test suite for OutputGenerator."""

    def test_generate_yaml_single_trade(self) -> None:
        """Should generate valid YAML for single trade."""
        trades = [Trade(day=1, action="buy", asset_id="asset_1")]

        yaml_str = OutputGenerator.generate_yaml(trades)

        # Parse to verify valid YAML
        data = yaml.safe_load(yaml_str)
        assert 1 in data
        assert data[1] == [{"buy": "asset_1"}]

    def test_generate_yaml_multiple_trades_same_day(self) -> None:
        """Should group multiple trades on same day."""
        trades = [
            Trade(day=1, action="buy", asset_id="asset_1"),
            Trade(day=1, action="buy", asset_id="asset_2"),
        ]

        yaml_str = OutputGenerator.generate_yaml(trades)
        data = yaml.safe_load(yaml_str)

        assert 1 in data
        assert len(data[1]) == 2
        assert {"buy": "asset_1"} in data[1]
        assert {"buy": "asset_2"} in data[1]

    def test_generate_yaml_multiple_days(self) -> None:
        """Should handle trades on different days."""
        trades = [
            Trade(day=1, action="buy", asset_id="asset_1"),
            Trade(day=5, action="buy", asset_id="asset_2"),
            Trade(day=10, action="sell", asset_id="asset_1"),
        ]

        yaml_str = OutputGenerator.generate_yaml(trades)
        data = yaml.safe_load(yaml_str)

        assert 1 in data
        assert 5 in data
        assert 10 in data
        assert data[1] == [{"buy": "asset_1"}]
        assert data[5] == [{"buy": "asset_2"}]
        assert data[10] == [{"sell": "asset_1"}]

    def test_save_output_creates_file(self, tmp_path: Path) -> None:
        """Should create output file."""
        trades = [Trade(day=1, action="buy", asset_id="asset_1")]
        output_file = tmp_path / "output.yml"

        OutputGenerator.save_output(trades, str(output_file))

        assert output_file.exists()

    def test_save_output_valid_yaml(self, tmp_path: Path) -> None:
        """Saved file should contain valid YAML."""
        trades = [
            Trade(day=1, action="buy", asset_id="asset_1"),
            Trade(day=5, action="buy", asset_id="asset_2"),
        ]
        output_file = tmp_path / "output.yml"

        OutputGenerator.save_output(trades, str(output_file))

        with open(output_file) as f:
            data = yaml.safe_load(f)

        assert 1 in data
        assert 5 in data

    def test_generate_yaml_preserves_order(self) -> None:
        """Should maintain day order in output."""
        trades = [
            Trade(day=1, action="buy", asset_id="asset_1"),
            Trade(day=15, action="buy", asset_id="asset_4"),
            Trade(day=30, action="buy", asset_id="asset_10"),
        ]

        yaml_str = OutputGenerator.generate_yaml(trades)
        data = yaml.safe_load(yaml_str)

        days = list(data.keys())
        assert days == [1, 15, 30]
