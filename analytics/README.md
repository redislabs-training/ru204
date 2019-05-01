# Analytics

## grade_loader.py / grade_loader.sh
This utility is used to take a CSV file generated for a given course & run and load this into RedShift.

### grade_loader.py
Python loader to load a single file

```python3 grade_loader.py <password> <course> <run> <path/to/csv/file>```

e.g.

```python3 grade_loader.py foobar RU101 2019_02 /src/lms/redislabs_RU101_2019_02_grade_report.csv```

### grade_loader.sh
This is used to load mutiple files, usage

```grade_loader.sh <password> <path/to/files>```

e.g.

```grade_loader.sh foobar /src/lms/new/```


### redshift-laoder.py
Thsi is used to take the CSV fiel provided by Appsembler for course enrollments to upload into RedShift. This is no longer required, since the registration and enrollment events are now fed directly (via Segment) into the LMS.