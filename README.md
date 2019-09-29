__________________________________________________________________________
                                Cron Parser
__________________________________________________________________________

The script scans a cron string and produces the cron table indicating 
when a specific command will be executed

| Field        | Required | Allowed values  | Allowed special characters |
|--------------|----------|-----------------|----------------------------|
| Minutes      | Yes      | 0–59            | * , - /                    |
| Hours        | Yes      | 0–23            | * , - /                    |
| Day of month | Yes      | 1–31            | * , - /                    |
| Month        | Yes      | 1–12 or JAN–DEC | * , - /                    |
| Day of week  | Yes      | 0–6 or SUN–SAT  | * , - /                    |
| Command      | Yes      | ANY             | ANY                        |


Example of output for "2 3-10 2/22 JUN,SEP,OCT,NOV * /usr/bin/find"

minute        2
hour          3 4 5 6 7 8 9 10
day of month  2 24
month         6 9 10 11
day of week   0 1 2 3 4 5 6
command       /usr/bin/find


__________________________________________________________________________
                                Python Version
__________________________________________________________________________
                                
It is necessary to use any version 3.x


__________________________________________________________________________
                                  Solution
__________________________________________________________________________

The solution consists of the main.py that reads the user input and of the
CronParser class able to parse a cron string.
The class can easily be extented to manage further cases.

Some examples of inputs

- "*/15 0 1,15 1-12 0-6 /usr/bin/find"
- "*/15 0 1,15 JAN-DEC SUN-SAT /usr/bin/find"
- "*/15 0 1,15 2/3 3/2 /usr/bin/find"
- "*/15 0 1,15 FEB/3 WED/2 /usr/bin/find"
- "2/5 0 1,15 MAR,APR,MAY MON,TUE,THU,FRI /usr/bin/find"
- "2 3-10 2/22 JUN,JUL,AUG,SEP,OCT,NOV * /usr/bin/find"


__________________________________________________________________________
                                 Unit Tests
__________________________________________________________________________

There are unit tests covering most of the code paths. In order to run the
unit tests, it is possible to use the command

- python -m unittest discover -p "*_test.py"

