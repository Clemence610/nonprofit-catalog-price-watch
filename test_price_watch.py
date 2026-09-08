from price_watch import CatalogObservation, reminder_for


def test_reminder_marks_material_competitor_drop():
    assert reminder_for(CatalogObservation("gloves", 10.0, 8.9)) is True
    assert reminder_for(CatalogObservation("gloves", 10.0, 9.1)) is False
