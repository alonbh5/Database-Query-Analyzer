# Database-Query-Analyzer
DataBase Query Validator and Parser - for DB course of 3th Year

for DB:
Customers(Name: STRING, Age: INTEGER)
Orders(CustomerName: STRING, Product: STRING, Price: INTEGRER)

SQL PARSING

Input - SQL Query in the form of "SELECT <> FROM <> WHERE <>;"

  WHERE - Supported ops: ),(,=,<,>,=>,=<,AND,OR
  WHERE - Not Supported ops: MAX,COUNT,MIN,JOIN,ORDERBY,...
  
  - Whitespace-Agnostic

Output - Does The Query Is a Valid SQL Query - By BNF algorithm

* no Regex,PCRE
