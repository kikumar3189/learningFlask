DROP TABLE if EXISTS users;
    CREATE TABLE users (
    id INTEGER PRIMARY KEY autoincrement,
    firstname text,
    lastname text,
    email NOT NULL UNIQUE,
    password text NOT NULL

);

CREATE TABLE user_tiffin (

email text ,
timing text,
type text,
size text,
address text,
status text,
PRIMARY KEY (email, timing),
CONSTRAINT fk_email FOREIGN KEY (email) REFERENCES users(email)
);

CREATE TABLE user_address (
email text ,
address_name text ,
address_line1 text,
address_line2 text,
city text,
pin_code integer ,
PRIMARY KEY (email, address_name),
CONSTRAINT fk_email FOREIGN KEY (email) REFERENCES users(email)

)