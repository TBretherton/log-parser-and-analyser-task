# log-parser-and-analyser-task

This application parses the CSV log file `logs[7].log` identifying each job or task and tracks its start and finish times.

It calculates the duration of each job and logs this information at different levels depending on the duration:
- If the job is under 5 minutes the log level will be `info`.
- If the job is between 5 and 10 minutes the log level will be `warning`.
- If the job is over 10 minutes the log level will be `error`.

The application also does some data validation on the log lines and checks for jobs with an end but no start,and jobs with a start but no end and jobs with other statuses

There are tests that cover this functionality located in `log_test.py`

There is also basic CI to run this application located in `.github/workflows/ci.yml`

You can see the outcome of this application running in CI [here](https://github.com/TBretherton/log-parser-and-analyser-task/actions)