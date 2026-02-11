from src.pipelines.engine import get_status


def test_pipeline_status() -> None:
    assert get_status() == "initialized"
