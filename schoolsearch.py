#!/usr/bin/python

import sys
import time

'''
Class that represents a database query, either specified from the command line
or entered in interpreter mode.
'''
class Query(object):
  class Type:
    STUDENT = 0
    STUDENT_BUS = 1
    TEACHER = 2
    GRADE = 3
    BUS = 4

  '''
  type_: The Type of this Query.
  arg: The argument to query with type |type_|
  '''
  def __init__(self, type_, arg):
    self.type_ = type_
    self.arg = arg

  '''
  Returns True if this Query matches Record |record|, False otherwise.

  record: The record to compare this Query to.
  '''
  def MatchesRecord(self, record):
    if (((self.type_ == Query.Type.STUDENT or
          self.type_ == Query.Type.STUDENT_BUS) and
        self.arg != record.studentLast) or
        (self.type_ == Query.Type.TEACHER and self.arg != record.teacherLast) or
        (self.type_ == Query.Type.GRADE and self.arg != record.grade) or
        (self.type_ == Query.Type.BUS and self.arg != record.bus)):
      return False
    return True

'''
Class that represents one record in the database.
'''
class Record(object):
  '''
  record: One line from the database file. Has the form:
      studentLast,studentFirst,grade,classroom,bus,teacherLast,teacherFirst
  '''
  def __init__(self, record):
    self.record = record.split(',')

  @property
  def studentLast(self):
    return self.record[0]

  @property
  def studentFirst(self):
    return self.record[1]

  @property
  def grade(self):
    return self.record[2]

  @property
  def classroom(self):
    return self.record[3]

  @property
  def bus(self):
    return self.record[4]

  @property
  def teacherLast(self):
    return self.record[5]

  @property
  def teacherFirst(self):
    return self.record[6]

  '''
  Converts this Record to a string, according to the type of Query that matched
  this Record.

  type_: The type of Query that matched this Record.
  '''
  def ToString(self, type_):
    if type_ == Query.Type.STUDENT:
      return '%s, %s, %s, %s' % (self.studentLast, self.studentFirst,
                                 self.grade, self.classroom)
    elif type_ == Query.Type.STUDENT_BUS:
      return '%s, %s, %s' % (self.studentLast, self.studentFirst, self.bus)
    elif type_ == Query.Type.TEACHER or type_ == Query.Type.GRADE:
      return '%s, %s' % (self.studentLast, self.studentFirst)
    elif type_ == Query.Type.BUS:
      return '%s, %s, %s' % (self.studentLast, self.studentFirst,
                             self.classroom)
    else:
      print 'Unknown query type "%s"' % type_
      return

'''
Handles a database query of one of the following forms, printing the matching
records to sys.stdout:

  S[tudent]: <lastname> [B[us]]
  T[eacher]: <lastname>
  G[rade]: <number>
  B[us]: <number>
'''
def HandleQuery(args):
  if not len(args):
    print 'Missing query arguments'
    return

  if args[0] == 'S:' or args[0] == 'Student:':
    if len(args) == 2:
      query = Query(Query.Type.STUDENT, args[1])
    elif len(args) == 3:
      if args[2] == 'B' or args[2] == 'Bus':
        query = Query(Query.Type.STUDENT_BUS, args[1])
      else:
        print 'Unknown argument to "%s": "%s". %s' % (
            args[0],
            args[2],
            SyntaxString(Query.Type.STUDENT))
        return
    else:
      print 'Missing argument to "%s". %s' % (
          args[0],
          SyntaxString(Query.Type.STUDENT))
      return
  elif args[0] == 'T:' or args[0] == 'Teacher:':
    if len(args) == 2:
      query = Query(Query.Type.TEACHER, args[1])
    else:
      print 'Missing argument to "%s". %s' % (
          args[0],
          SyntaxString(Query.Type.TEACHER))
      return
  elif args[0] == 'G:' or args[0] == 'Grade:':
    if len(args) == 2:
      query = Query(Query.Type.GRADE, args[1])
    else:
      print 'Missing argument to "%s". %s' % (
          args[0],
          SyntaxString(Query.Type.GRADE))
      return
  elif args[0] == 'B:' or args[0] == 'Bus:':
    if len(args) == 2:
      query = Query(Query.Type.BUS, args[1])
    else:
      print 'Missing argument to "%s". %s' % (
          args[0],
          SyntaxString(Query.Type.BUS))
      return
  else:
    print 'Unknown query type "%s"' % args[0]
    return

  PrintMatches(query)

'''
Given a Query, iterates through the database, printing all Records that match
Query |query|.

query: The query to match Records against.
'''
def PrintMatches(query):
  records = []
  timeBefore = time.time()
  for line in open('students.txt'):
    record = Record(line)
    if query.MatchesRecord(record):
      records.append(record)
  for record in records:
    print record.ToString(query.type_)
  print '(Took %f seconds)' % (time.time() - timeBefore)


'''
Returns the syntax of Query with Type |type_|.

type_: The Query's Type.
'''
def SyntaxString(type_):
  try:
    return {
      Query.Type.STUDENT: 'Syntax: S[tudent]: <lastname> [B[us]]',
      Query.Type.STUDENT_BUS: 'Syntax: S[tudent]: <lastname> [B[us]]',
      Query.Type.TEACHER: 'Syntax: T[eacher]: <lastname>',
      Query.Type.GRADE: 'Syntax: G[rade]: <number>',
      Query.Type.BUS: 'Syntax: B[us]: <number>',
    }[type_]
  except KeyError:
    print 'Type %s missing syntax definition' % type_
    return

def PrintInteractiveHelp():
  print 'Valid queries:'
  print '  S[tudent]: <lastname> [B[us]]'
  print '  T[eacher]: <lastname>'
  print '  G[rade]: <number>'
  print '  B[us]: <number>'
  print 'Enter Q[uit] to quit.'

def main():
  # Batch mode.
  if len(sys.argv) > 1:
    HandleQuery(sys.argv[1:])
    return

  # Interactive mode.
  PrintInteractiveHelp()
  line = sys.stdin.readline().strip()
  while line != 'Q' and line != 'Quit':
    HandleQuery(line.split())
    line = sys.stdin.readline().strip()

if __name__ == '__main__':
  main()
