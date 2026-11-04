# Inventory: nightly photo backup (known-good fixture)

| Name | Is | Made by, from | Current | Lives | Status | Source |
|---|---|---|---|---|---|---|
| backup script | program that copies photos changed since its last run | the household admin, by hand | runs each night when the schedule starts it | laptop, ~/bin/backup.sh | exists | backup.sh line 1 |
| schedule | task-list line that starts the backup script at 02:00 | the household admin, with crontab | fixed; changes only by hand | laptop crontab | exists | crontab -l |
| backup disk | external drive that holds the copies | the backup script, from the laptop's photos | at most one day old | external USB drive | exists | log file line 212 |
| log file | text file with one line per run | the backup script, at the end of each run | one line per night | backup disk, backup.log | exists | backup.log |

## Picture plan

| Section | Kind | Caption or reason |
|---|---|---|
| One night | real output | The log file line for 3 November: 14 photos copied, no errors. |
| The parts | diagram | Only photos move: the backup script never changes the laptop's own files. |
| A run, step by step | animation | Each run has two steps, and only the second one touches the backup disk. |
| Checking it worked | none | one sentence says it as fast |
