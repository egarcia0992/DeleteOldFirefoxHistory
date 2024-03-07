import os
import sqlite3
from datetime import datetime, timedelta
# Firefox app must be closed before running


def delete_old_firefox_history():
    profile_directory = os.path.expanduser("~/Library/Application Support/Firefox/Profiles/")
    if not os.path.exists(profile_directory):
        print("Firefox profile directory NOT found.")
        return

    profile_path = ""
    for directory in os.listdir(profile_directory):
        if directory.endswith(".default-release"):
            # most forums use ".default" but it only worked with ".default-release" on my system
            profile_path = os.path.join(profile_directory, directory)
            break

    ff_database = os.path.join(profile_path, 'places.sqlite')

    if not os.path.exists(ff_database):
        print("Error finding Firefox database.")
        return

    try:
        connection = sqlite3.connect(ff_database)
        cursor = connection.cursor()

        history_time = datetime.now() - timedelta(days=7)
        # determines the time cutoff for history items
        cursor.execute("DELETE FROM moz_places WHERE last_visit_date < ?",
                       (history_time.timestamp() * 1000000,))

        connection.commit()
        connection.close()
        print("Old History Items Deleted")

    except sqlite3.Error as e:
        print("SQLite error: ", e)

    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    delete_old_firefox_history()
