# SQliteLearning

This repository is dedicated to learning different aspects and functions of SQLite. It will contain various small projects aimed at exploring SQLite functionalities.

## Projects Included:

### 1. hello_SQLite

- **Description:** 
  - This project marks my initial foray into SQLite3. It utilizes Pyside6 for the UI.
  - The database includes an "employee" table storing first names, last names, and salaries.
  - Users can add, edit salary, and remove employees via the UI.
  - The UI displays a table of all employees, featuring columns for full name, email, and salary.

- **YouTube Tutorial Reference:** 
  - This project is based on a tutorial, though significant modifications have been made.
  - [YouTube Tutorial Link](https://www.youtube.com/watch?v=pd-0G0MigUA&ab_channel=CoreySchafer)

### 2. Trading_bot_tables

- **Description:** 
  - This project is the primary motivation for learning SQLite3.
  - It is intended for integration into the Crypto Trading Platform.
  - The project adheres to the database diagram available at [this link](https://github.com/agordon05/Trading-Bot/blob/main/Documents/DatabaseDiagram.jpg).
  - Comprising 12 tables: `Timeframe`, `Status`, `Exchange_Type`, `Strategy_Type`, `Grid_Strategy_Param`, `Strategy_Param_Link`, `Strategy_Settings`, `Exchange_Keys`, `Contract`, `Exchange`, `Bot`, and `Trade`.
  - It includes methods for efficiently retrieving information from and adding to these tables.
  - Test cases are actively being added to ensure functionality.
