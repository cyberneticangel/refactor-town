def summarize(readings):
    """Summarize temperature readings, ignoring negative values (sensor errors)."""
    valid = [reading for reading in readings if reading >= 0]
    if not valid:
        return {"count": 0, "total": 0, "average": 0, "highest": None}

    total = sum(valid)
    return {
        "count": len(valid),
        "total": total,
        "average": total / len(valid),
        "highest": max(valid),
    }
