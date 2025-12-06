# budgetbuddy/data/repository.py

import json
from pathlib import Path

from budgetbuddy.core.models import UserProfile


# Main data file used by the application
DATA_FILE = Path("budgetbuddy/budgetbuddy_data.json")


class ProfileDataError(Exception):
    """Raised when the profiles data file cannot be read or parsed."""
    pass


def load_profiles():
    """
    Load all profiles from DATA_FILE.

    Returns a dict mapping profile name -> UserProfile.

    Raises:
        ProfileDataError: if the JSON file is corrupted or cannot be read.
    """
    if not DATA_FILE.exists():
        # No data file yet – return empty profiles dict
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        # File exists but contains invalid JSON
        raise ProfileDataError(f"Data file {DATA_FILE} is corrupted.") from e
    except OSError as e:
        # Permission / I/O issues
        raise ProfileDataError(f"Could not read data file {DATA_FILE}.") from e

    profiles = {}
    for name, pdata in raw.items():
        profile = UserProfile.from_dict(pdata)
        profiles[name] = profile
    return profiles


def save_profiles(profiles):
    """
    Save all profiles to DATA_FILE.

    profiles: dict mapping name -> UserProfile
    """
    data = {name: profile.to_dict() for name, profile in profiles.items()}

    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        # For CLI use we just print an error message
        print(f"Error: could not save data to {DATA_FILE}: {e}")


def create_profile(profiles, name):
    """
    Create a new UserProfile with the given name and add it to profiles dict.

    Returns the new UserProfile instance.
    """
    profile = UserProfile(name)
    profiles[name] = profile
    return profile


def rename_profile(profiles, old_name, new_name):
    """
    Rename a profile key in the dict and update the profile.name field.
    """
    if old_name not in profiles:
        return

    profile = profiles.pop(old_name)
    profile.name = new_name
    profiles[new_name] = profile


def delete_profile(profiles, name):
    """
    Remove a profile from the dict if it exists.
    """
    if name in profiles:
        del profiles[name]
