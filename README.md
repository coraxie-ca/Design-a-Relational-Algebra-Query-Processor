# Design-a-Relational-Algebra-Query-Processor
- A system similar to RelaX that can accept text representing relations and relational algebra queries, then execute and display the results.
- RelaX: https://dbis-uibk.github.io/relax/calc/local/uibk/local/0

# operator format
- select：select [condition] (table)
- project: project [condition] (table)
- join: (table_1) join [condition] (table_2)
- intersect: A x B 
- union: A u B
- minus: A - B

# query samples:
- query: select Age>20 Student
- query: project Name,Age Student
- query: Student join Student.ID=Enrollment.StudentID Enrollment

# nested query:
- query: project Name,Age (StudentA intersect Student)
- query: (select Age>21 Student) union (select Age<21 Student)
- query: project Name,Age (select Age>20 (StudentA minus Student))
- query: project Name,Age ((select Age<=21 Student) join Student.ID=Enrollment.StudentID Enrollment)

# rules of query:
- no space within a condition: Age>20
- enclose nested query inside bracket ()

# rules of table:
- first line: <table name> = {
- second line: <arg1>, <arg2>, ...
- left lines: data
- last line: }
- no space within any table data
