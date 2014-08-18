# Fogbugz Util

A script to facilitate common Fogbugz interactions from the command line.

Feel free to add to, modify, change, make better as you see fit.

Available Commands:

* List active cases by user
* Work on a case
* Stop Work
* Set Estimate on a case
* Set non-timesheet elapse time on a case
* Comment on a case
* list cases by project
* resolve case

## Set up

In the `fb_settings.py`, change the `token` value to your token.

Go to this address: `http://fogbugz.domain.org/api.asp?cmd=logon&email=USERNAME&password=PASSWORD`

Use your username, not email for `USERNAME`. If your password has any reserved characters, you will need to find the appropriate code for them. For example, `&` = `%26`.

Install the Python module `fogbugz` with `pip`. `pip install fogbugz`

## Usage

`python main.py [options]`

Valid options:

* `-l [USER]`
  * ex. `-l "Todd Waits"`
  * Returns all *active* cases assigned to specified user.
* `-w [CASE NUMBER]`
  * ex. `-w 1304`
  * Starts work timer on specified case
* `-s`
  * Stops work timer.
* `-e [HOURS] [CASE NUMBER]`
  * ex. `-e 2 1304` sets case 1304 estimate to 2 hours
  * Sets estimate of specified case
* `-t [HOURS] [CASE NUMBER]`
  * ex. `-e 1 1304` sets non-timesheet elapsed time for case 1304 to 1 hour
  * What ever number is entered will **OVERWRITE** the elapsed time for the specified case.
  * Does not affect timesheet time.
  * If the current elapsed time is 2 hours, and you write 1 (thinking you are adding 1 hour), you will overwrite 2 hours with 1.
* `-c [COMMENT] [CASE NUMBER]`
  * ex. `-c "Working on a bunch of stuff" 1304`
  * This will add the comment `Working on a bunch of stuff` to case 1304.
* `-p [USER]`
  * ex. `-p "Todd Waits"`
  * Lists all active cases assigned to Todd Waits in all projects, and displays them by project.
* `-r [CASE NUMBER]`
  * ex. `-r 1304`
  * Resolves case 1304.

## Future Work

* list cases by due date / milestone
* new case (title, project)
* Token-based authentication

## Output of `-h`

```
usage: main.py [-h] [-s] [-w WORKING] [-l USER] [-m N N] [-t N N]
               [-c COMMENT COMMENT]

Interact with FogBugz.

optional arguments:
  -h, --help            show this help message and exit
  -s, --stop            Stop working on a case.
  -w WORKING, --working WORKING
                        Start working on case [n]
  -l USER, --list USER  List all active cases by USER.
  -e N N, --estimate N N
                        Set ESTIMATE on a CASE NUMBER.
  -t N N, --time N N    Set TIME on CASE NUMBER. !!WARNING!! Overwrites value,
                        does not add!
  -c COMMENT COMMENT, --comment COMMENT COMMENT
                        Add a COMMENT on CASE NUMBER.
  -p USER, --project USER
                        List all active cases for USER for each project.
  -r CASE NUMBER, --resolve CASE NUMBER
                        Resolve specified case.
```

# fb_pullReqs.py

From commandline, run `python fb_pullReqs.py -p "[PROJECT NAME]"`. This will connect to the FogBugz instance defined in your fb_settings.py file and create a Markdown formatted file in the current working directory of all tasks of category "Requirement". 

This an easy way to create a simple requirements document that is primarily edited and maintained in the FogBugz instance.