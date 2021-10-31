-- DROP TABLES IF YOU ARE SURE THEY EXIST OR YOU ARE OKAY TO SEE ERRORS:
drop table kart;
drop table products;
drop table users;
drop table categories;


--DROP TABLE IF THEY EXIST (no error message if they dont exist): 
begin
   execute immediate 'drop table kart';
exception
   when others then null;
end;
/

begin
   execute immediate 'drop table products';
exception
   when others then null;
end;
/

begin
   execute immediate 'drop table users';
exception
   when others then null;
end;
/

begin
   execute immediate 'drop table categories';
exception
   when others then null;
end;
/


-- Creating the tables required for the application:

CREATE TABLE users(
	userId NUMBER(10),
	password varchar2(255),
	email varchar2(255),
	firstName varchar2(255),
	lastName varchar2(255),
	address1 varchar2(255),
	address2 varchar2(255),
	zipcode varchar2(255),
	city varchar2(255),
	state varchar2(255),
	country varchar2(255),
	phone varchar2(255),
	PRIMARY KEY(userId));


CREATE TABLE categories(
	categoryId NUMBER(10),
	name varchar2(255),
	PRIMARY KEY(categoryId));



CREATE TABLE products(
	productId NUMBER(10),
	name varchar2(255),
	price BINARY_DOUBLE,
	description varchar2(255),
	image varchar2(255),
	stock NUMBER(10),
	categoryId NUMBER(10),
	FOREIGN KEY(categoryId) REFERENCES categories(categoryId),
	PRIMARY KEY(productId));



CREATE TABLE kart(userId NUMBER(10),
	productId NUMBER(10),
	FOREIGN KEY(userId) REFERENCES users(userId),
	FOREIGN KEY(productId) REFERENCES products(productId));

             
-- Inserting data into tables:

INSERT INTO users(userId, password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) 
VALUES
('1', '0cc175b9c0f1b6a831c399e269772661', 'abcd@example.com', 'Harsh', 'Shah', 'scaa', 'asa', 'as', 'asc', 'dasd', 'dfas', 'dsa');


INSERT INTO categories(categoryId, name) 
SELECT 1, 'Men' FROM dual UNION ALL 
SELECT 2, 'Books' FROM dual UNION ALL 
SELECT 3, 'Computers and Accessories' FROM dual UNION ALL
SELECT 4, 'Movies, Music and Video Games'FROM dual UNION ALL 
SELECT 5, 'Jwelery, Watches and Eyewear' FROM dual UNION ALL 
SELECT 6, 'Women' FROM dual;


INSERT INTO products(productId, name, price, description, image, stock, categoryId) 
	 SELECT 2, 'Second', '2.0', 'Second Item', 'Kinkaku_Ji_by_Elizabeth_K_Joseph.jpg', 2, 1 FROM dual UNION ALL 
	 SELECT 3, 'First', '1.0', 'First book.', 'Untitled_by_Troy_Jarrell.jpg', 1, 2 FROM dual UNION ALL 
	 SELECT 4, 'T Shirt 1', '1.0', 'First T shirt', 'Kinkaku_Ji_by_Elizabeth_K_Joseph.jpg', 1, 1 FROM dual UNION ALL 
	 SELECT 5, 'T Shirt 2', '2.0', 'Second T shirt', 'The_Sky_Is_The_Limit_by_Kaushik_Panchal.jpg', 2, 1 FROM dual UNION ALL 
	 SELECT 6, 'T Shirt 3', '3.0', 'Third tshirt', 'Untitled_by_Troy_Jarrell.jpg', 3, 1 FROM dual UNION ALL 
	 SELECT 7, 'T Shirt 4', '4.0', 'Fourth T shirt', 'Untitled_by_Aaron_Burden.jpg', 4, 1 FROM dual UNION ALL 
	 SELECT 8, 'T Shirt 5', '5.0', 'FIfth Tshirt', 'The_Sky_Is_The_Limit_by_Kaushik_Panchal.jpg', 5, 1 FROM dual UNION ALL 
	 SELECT 9, 'Book 1', '1.0', 'FIrst Book', 'Mountainous_View_by_Sven_Scheuermeier.jpg', 1, 2 FROM dual UNION ALL 
	 SELECT 10, 'Book 2', '2.0', 'Second Book', 'The_Sky_Is_The_Limit_by_Kaushik_Panchal.jpg', 2, 2 FROM dual UNION ALL 
	 SELECT 11, 'Book 3', '3.0', 'Third book.', 'Untitled_0026_by_Mike_Sinko.jpg', 3, 2 FROM dual UNION ALL 
	 SELECT 12, 'Book 4', '4.0', 'Fourth book.', 'Untitled_7019_by_Mike_Sinko.jpg', 4, 2 FROM dual UNION ALL 
	 SELECT 13, 'Book 5', '5.0', 'Fifth book.', 'Untitled_by_Troy_Jarrell.jpg', 5, 2 FROM dual UNION ALL 
	 SELECT 14, 'Computer 1', '1.0', 'First computer', 'Untitled_by_Aaron_Burden.jpg', 1, 3 FROM dual UNION ALL 
	 SELECT 15, 'Movie 1', '1.0', 'First mvoie', 'Yellow_Jacket_by_Manuel_Frei.png', 1, 4 FROM dual UNION ALL 
	 SELECT 16, 'Jwelery 1', '1.0', 'First jwelery', 'Kinkaku_Ji_by_Elizabeth_K_Joseph.jpg', 1, 5 FROM dual UNION ALL 
	 SELECT 17, 'Saree 1', '1.0', 'First saree', 'Mountainous_View_by_Sven_Scheuermeier.jpg', 1, 6 FROM dual;



-- Commands to test the database:

select * from users;
select * from products;
select * from kart;
select * from categories;

desc users;
desc products;
desc kart;
desc categories;
