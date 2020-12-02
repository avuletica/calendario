import itertools
from datetime import timedelta
from typing import List, Generator, Tuple, Any


def datetime_range(start=None, end=None) -> Generator:
    span = end - start
    for i in range(span.days + 1):
        yield start + timedelta(days=i)


def is_intersection(x: List, y: List) -> bool:
    result = set(x).intersection(set(y))
    return bool(result)


def max_intersections(*args) -> Any:
    intersections = []
    for a, b in itertools.combinations(args, 2):
        intersections.append(is_intersection(a, b))

    if not intersections:
        return None

    return intersections.index(max(intersections))


def eliminate_overlaps(*args) -> dict:
    args = list(args)

    datetime_ranges = [item["availability_range"] for item in args]
    most_intersections_index = max_intersections(*datetime_ranges)

    # If there are no intersections handle first
    if most_intersections_index is None:
        availability_range = sorted(args[0]["availability_range"])
        return {
            "apartments": [args[0]["apartment_name"]],
            "next_cleaning_time": availability_range[-1],
        }

    # Intersection base will be a list with the most number of intersections.
    base = args.pop(most_intersections_index)
    ret_value = {
        "apartments": [base["apartment_name"]],
        "next_cleaning_time": set(base["availability_range"]),
    }

    # Since we only know the list with most intersection and we don't know which list intersect with which list
    # We must check intersection before applying it to base
    for item in args:
        if is_intersection(ret_value["next_cleaning_time"], item["availability_range"]):
            temp = ret_value["next_cleaning_time"].intersection(
                set(item["availability_range"])
            )
            ret_value["next_cleaning_time"] = temp
            ret_value["apartments"].append(item["apartment_name"])

    latest_cleaning_time = sorted(ret_value["next_cleaning_time"])
    ret_value["next_cleaning_time"] = latest_cleaning_time[-1]
    return ret_value


def calculate_availability(apartment_entries: List[dict]) -> Tuple[list, list]:
    """
        Calculate datetime ranges when apartments are unoccupied.
    """
    entries_to_pop = []
    next_cleaning_time = []
    available_apartment_dates = []
    for index, calendar_entry in enumerate(apartment_entries):
        if index + 1 == len(apartment_entries):
            break
        end_time = apartment_entries[index]["end_datetime"]
        next_start_time = apartment_entries[index + 1]["start_datetime"]

        # If next booking is at same day clean immediately
        if next_start_time.day == end_time.day:
            next_cleaning_time.append(
                next_start_time.replace(hour=11)
            )
            entries_to_pop.append(index)
            continue

        datetime_range_ = list(datetime_range(end_time, next_start_time))
        available_apartment_dates.append(datetime_range_)

    for item in entries_to_pop:
        apartment_entries.pop(item)

    available_apartment_dates.sort()
    return available_apartment_dates, next_cleaning_time
