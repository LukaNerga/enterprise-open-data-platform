"""
lecture 6 (დამატება): Slowly Changing Dimension (SCD) Type 2 — testable ლოგიკა.
Star Schema-ს (Step 1-7) dim_location-ისთვის — თუ ლოკაციის ატრიბუტი შეიცვალა,
ძველი row 'იხურება' (is_current=False), ახალი emerges (is_current=True) —
ისტორია არასდროს იშლება, ჩაწერის ნაცვლად ახალი ვერსია ემატება.
"""


def scd2_upsert(existing_rows: list, new_version: dict, key_field: str, tracked_fields: list,
                effective_date: str) -> list:
    """
    SCD Type 2 upsert:
    - თუ key_field-ის მიხედვით row არ არსებობს → პირველი ვერსია ემატება.
    - თუ არსებობს და tracked_fields არ შეცვლილა → არაფერი იცვლება.
    - თუ არსებობს და tracked_fields შეიცვალა → ძველი row იხურება (is_current=False,
      valid_to=effective_date), ახალი emerges (is_current=True, valid_from=effective_date).
    """
    key_value = new_version[key_field]
    current_row = next(
        (r for r in existing_rows if r[key_field] == key_value and r.get("is_current")), None
    )

    if current_row is None:
        new_row = {**new_version, "valid_from": effective_date, "valid_to": None, "is_current": True}
        return existing_rows + [new_row]

    changed = any(current_row.get(f) != new_version.get(f) for f in tracked_fields)
    if not changed:
        return existing_rows

    updated_rows = [
        {**r, "valid_to": effective_date, "is_current": False} if r is current_row else r
        for r in existing_rows
    ]
    new_row = {**new_version, "valid_from": effective_date, "valid_to": None, "is_current": True}
    return updated_rows + [new_row]
if __name__ == "__main__":
    rows = []

    # Test 1
    rows = scd2_upsert(
        rows,
        {"city": "Tbilisi", "population_category": "large"},
        "city",
        ["population_category"],
        "2026-01-01"
    )
    print("Test 1:", rows)

    # Test 2
    rows = scd2_upsert(
        rows,
        {"city": "Tbilisi", "population_category": "large"},
        "city",
        ["population_category"],
        "2026-06-01"
    )
    print("Test 2:", rows)

    # Test 3
    rows = scd2_upsert(
        rows,
        {"city": "Tbilisi", "population_category": "mega"},
        "city",
        ["population_category"],
        "2026-09-01"
    )
    print("Test 3:", rows)

    assert len(rows) == 2
    assert rows[0]["is_current"] is False
    assert rows[1]["is_current"] is True

    print("\n[OK] All 3 scenarios passed!")