# E-Commerce Application

This e-commerce application provides a microservices-based architecture for managing products and orders. It is built using Flask and SQLite, and it includes Docker support.

## Features

### Product Management
- **Add Products:** Create new products with details such as name, description, price, and stock.
- **Retrieve Products:** List all products or get details of a specific product.
- **Update Products:** Modify the details of an existing product.
- **Delete Products:** Remove products from the system.

### Order Management
- **Create Orders:** Place orders for products.
- **Retrieve Orders:** View all orders for a specific user or details of a particular order.
- **Update Orders:** Change the status of an order.
- **Delete Orders:** Remove orders from the system.

### User mangement
- **Register user:** Register the new user with username, email and password.
- **Login user:** After registation user are able to login.

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Clear docker content](#clear-docker-content)

## Installation

Follow these steps to install and set up the application:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/adityabhalsod/E-Commerce-Backend-Engineering-Challenge
   cd E-Commerce-Backend-Engineering-Challenge
   ```

2. **Create a virtual environment:**

   ```sh
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Running the Application

To run the application locally:

1. **Set the Flask environment variables:**

   ```sh
   export SECRET_KEY=mysecretkey
   export SECRET_KEY=myjwtsecretkey  # On Windows use `set` instead of `export`
   ```

2. **Run the application:**
   ```sh
   flask run
   ```

Your application should now be running at `http://127.0.0.1:5000/`.

## Running Tests

To run the unit tests, use the following command:

```sh
cd user-auth-service && python -m unittest discover -s tests &&
cd ../product-management-service && python -m unittest discover -s tests &&
cd ../order-processing-service && python -m unittest discover -s tests
```

This command will execute all the test cases in the tests directory.

## Clear docker content

```sh
docker system prune -a
```
