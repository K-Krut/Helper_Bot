-- DROP DATABASE IF EXISTS finance; 
-- CREATE DATABASE finance;
DROP TABLE IF EXISTS budget;

USE finance;

CREATE TABLE budget (
	code_name varchar(50) PRIMARY KEY,
    daily_limit integer DEFAULT 0,
    month_limit integer DEFAULT 0
);
    
CREATE TABLE category(
	code_name varchar(100) PRIMARY KEY,
    category_name varchar(50),
    aliases_ text
);

CREATE TABLE expenses (
	expense_id integer NOT NULL AUTO_INCREMENT,
    amount integer,
    date_time datetime, 
    category varchar(100),
    PRIMARY KEY(expense_id),
    FOREIGN KEY (category) REFERENCES category(code_name)
);

CREATE TABLE incomes (
	income_id integer NOT NULL AUTO_INCREMENT,
    amount integer,
    date_time datetime,
    category varchar(100),
    PRIMARY KEY(income_id), 
    FOREIGN KEY (category) REFERENCES category(code_name)
);



