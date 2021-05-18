# Bookworm
**-A book review web application**

## Description

Users will be able to register on this website and then log in using their username and password.

Once he/she is logged in, they will be able to:-
- Search for books
    -  By their Title
    -  By their Author 
    -  By their ISBN number
- Add reviews for individual books
- View others reviews on a book.

## Used:

Third-party API by **Google Books APIs**, to pull in ratings from a broader audience.

**Postgreql database** in Amazon Webserver


## Things one can do in this Application:


1. Search a book with its Title

2. Search a book with its Author name

3. Search a book with it's ISBN number

4. View reviews from other BOOKWORMS

5. Add your own review

Initially if we don't have an account we have to create one by clicking the _**'Join Us'**_, and enter the necessary details in the form and click on the _**Signup**_ button now a new account ill be created. 

To log into the site we have to give the respective credentials. after undergoing verification you will be redirected to the home page of the web site


#### Searching a book by its's Title:


Type the book name in the text box. If you don't know the exact name of the book then its fine, partial input will also yield the result that contains the substring of the text that you have given as an input. All the books having a similar title will be displayed in a table format.on clicking on any of the titles of the book you will be redirected to a page that contains the information of the book along with the number of reviews and the average ratings given for the book data collected from the third party api.we can also view the comments of the other users and can also add you review and rating. From one login we can create only one review for a particular book more than one will through an error page.

**Similar to searching by the title we can search a book with it's ISBN number or its author.**

The logout button can be used to log out from a particular session.**

## Overview
![login page]()
![registeration]()
![home page]()
![book info]()
![Adding review]()

**If we use the route /api/< isbn> then we will be able to see the JSON response for the particular book**