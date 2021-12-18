DROP DATABASE IF EXISTS finance; 
CREATE DATABASE finance;

USE finance;

CREATE TABLE budget(
	code_name varchar(50) PRIMARY KEY,
    daily_limit integer,
    month_limit integer
);
    
CREATE TABLE category(
	code_name varchar(100) PRIMARY KEY,
    category_name varchar(50),
    aliases_ text
);

CREATE TABLE expenses(
	expense_id integer NOT NULL,
    amount integer,
    date_time datetime, 
    category varchar(100),
    message_text_ text, 
    CHECK (amount > -1),
    FOREIGN KEY (category) REFERENCES category(code_name)
);

CREATE TABLE incomes(
	income_id integer NOT NULL,
    amount integer,
    date_time datetime,
    category varchar(100),
    message_text_ text,
    CHECK (amount > -1),
    FOREIGN KEY (category) REFERENCES category(code_name)
);



