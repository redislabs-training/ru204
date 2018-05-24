import sys

def main(reg_file, enroll_file, dest_file):
  """Entry point to execute eithe rthe dump or load"""
  import csv
  import os
  from sets import Set

  reg = Set()
  enrolled = Set()
  students = {}
  try:
    with open(reg_file, 'rb') as csvfile:
      csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
      for row in csvreader:
        reg.add(row[2])
        students[row[2]] = row[0]
  finally:
    csvfile.close()

  try:
    with open(enroll_file, 'rb') as csvfile:
      csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
      for row in csvreader:
        enrolled.add(row[2])
  finally:
    csvfile.close()

  try:
    with open(dest_file, 'wb') as csvfile:
      csvwriter = csv.writer(csvfile, delimiter=',',
                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for match in reg - enrolled:
        if match in students:
          csvwriter.writerow([match, students[match]])
        else:
          print "No reg for {}".format(match)
  finally:
    csvfile.close()

  print "Regs {}".format(len(reg))
  print "Enrollments {}".format(len(enrolled))
  print "Students {}".format(len(students))

if __name__ == "__main__":
  main(sys.argv[1], sys.argv[2], sys.argv[3])