import sys

from discordBot import lastHourReminderMessage

if __name__ == "__main__":
    production = False  # fail to dev mode
    if len(sys.argv) > 1:
        # check if "production"
        if sys.argv[1] == "production":
            production = True

    lastHourReminderMessage(production)
