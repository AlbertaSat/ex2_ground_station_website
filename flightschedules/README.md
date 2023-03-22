# Flight Schedule Files

Here is where text files describing scheduled commands are generated.
These files are then to be automatically uploaded to the satellite by
comm.py through ex2_ground_station_software.

## Scheduled Command Format

Each scheduled command is separated by a new line character `\n`.
Each line is formatted in this way:

    {millisecond} {second} {minute} {hour} {dayOfWeek} {day} {month} {year} {command}

Example: `0 50 1 2 3 24 2 52 obc.time_management.get_time()`

Some Key Points:
- The day of the week starts at Sunday = 1
- The year is the offset from 1970 (eg. The year 2022 is set as 2022 - 1970 = 52)

## Repeating Commands
An asterick character `*` in any of these fields will schedule that command so that it repeats in every unit of that time.

Example: `  250 * 30 2 3 24 2 52 obc.time_management.get_time()`
- This command will be run in every second during the hour of 02:30 at the 250ms mark on 2022-02-24

If the **minute** field is repeating, then the **hour field will also repeat!!!**
