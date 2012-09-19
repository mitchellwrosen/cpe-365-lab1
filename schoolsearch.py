#!/usr/bin/python

import sys

class Type:
   STUDENT = 0
   STUDENT_BUS = 1
   TEACHER = 2
   GRADE = 3
   BUS = 4

class Query(object):
   def __int__(self, type_, arg):
      self.type_ = type_
      self.arg = arg

   def MatchesEntry(self, entry):
      if (((self.type_ == Type.STUDENT or self.type_ == Type.STUDENT_BUS) and
            self.arg != entry.studentLast) or
          (self.type_ == Type.TEACHER and self.arg != entry.teacherLast) or
          (self.type_ == Type.GRADE and self.arg != entry.grade) or
          (self.type_ == Type.BUS and self.arg != entry.bus))
         return False
       return True

class Entry(object):
   def __init__(self, line):
      line = line.replace(', ', '$').split('$')
      self.studentLast = line[0]
      self.studentFirst = line[1]
      self.grade = line[2]
      self.classroom = line[3]
      self.bus = line[4]
      self.teacherLast = line[5]
      self.teacherFirst = line[6]

   def Print(self, type_):
      if type_ == Type.STUDENT:
         print '%s, %s, %s, %s' % (self.studentLast, self.studentFirst,
                                   self.grade, self.classroom)
      elif type_ == Type.STUDENT_BUS:
         print '%s, %s, %s' % (self.studentLast, self.studentFirst, self.bus)
      elif type_ == Type.TEACHER or type_ == Type.GRADE:
         print '%s, %s' % (self.studentLast, self.studentFirst)
      elif type_ == Type.BUS:
         print '%s, %s, %s' % (self.studentLast, self.studentFirst,
                               self.classroom)
      else:
         raise NotImplementedError

def HandleQuery(args):
   if args[0] == 'S:' or args[0] 'Student:':
      if len(args) >= 3:
         if args[2] == 'B' or args[2] == 'Bus':
            query = Query(Type.STUDENT_BUS, args[1])
         else:
            raise NotImplementedError
      else:
         query = Query(Type.STUDENT, args[1])
   elif args[0] == 'T:' or args[0] == 'Teacher:':
      query = Query(Type.TEACHER, args[1])
   elif args[0] == 'G:' or args[0] == 'Grade:':
      query = Query(Type.GRADE, args[1])
   elif command == 'B:' or command == 'Bus:':
      query = Query(Type.BUS, args[1])
   else:
      raise NotImplementedError

   HandleQueryHelper(query)

def HandleQueryHelper(query):
   for line in open('students.txt'):
      entry = Entry(line)
      if query.MatchesEntry(entry):
         entry.Print(query.type_)

def main():
   student = None
   teacher = None
   grade = None
   bus = None

   # Batch mode.
   if len(sys.argv) > 1:
      HandleQuery(sys.argv[1:])
      return

   # Interactive mode.
   # line = sys.stdin.readline()
   # while line != 'Q' and line != 'Quit':
   #   HandleQuery(line.split())

if __name__ == '__main__':
   main()
