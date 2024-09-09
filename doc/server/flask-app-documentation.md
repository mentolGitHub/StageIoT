[retour à l'arborescence de la doc](../README.md)
# Flask Application Documentation

## Table of Contents
- [Flask Application Documentation](#flask-application-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup](#setup)
  - [Routes](#routes)
    - [Main Routes](#main-routes)
    - [Authentication Routes](#authentication-routes)
    - [Device Management Routes](#device-management-routes)
    - [Data Routes](#data-routes)
  - [Authentication](#authentication)
  - [Database Operations](#database-operations)
  - [API Endpoints](#api-endpoints)
  - [Utility Functions](#utility-functions)

## Introduction

This Flask application provides a web interface and API for managing IoT devices and their data. It includes user authentication, device registration, data visualization, and API endpoints for retrieving device data.

## Setup

The application uses the following main dependencies:
- Flask
- Flask-WTF
- Flask-HTTPAuth
- Flask-RESTful
- Flask-CORS
- MySQL Connector

To run the application:

```python
from queue import Queue
config = {...}  # Add your configuration here
IPnode(Queue(), config)
```

## Routes

### Main Routes

- `/`: Home page
- `/objects`: Objects page
- `/visualize`: Data visualization page
- `/map`: Map view page
- `/profile`: User profile page

### Authentication Routes

- `/login`: User login
- `/register`: User registration
- `/logout`: User logout

### Device Management Routes

- `/register_device`: Register a new device
- `/deviceList`: List user's devices
- `/edit_device/<deveui>`: Edit device details
- `/delete_device/<deveui>`: Delete a device

### Data Routes

- `/post_data`: Receive and process data from devices
- `/get_data`: Retrieve device data
- `/get_objects`: Get objects data
- `/get_euiList`: Get list of device EUIs
- `/downloadall`: Download all data as CSV
- `/download`: Download selected data as CSV
- `/objets_proches/<deveui>`: Get nearby objects for a device

## Authentication

The application uses session-based authentication for web routes and token-based authentication for API endpoints. Functions include:

- `verify_token(t)`: Verify authentication token
- `check_user_token()`: Check user token and return username
- `get_user_from_api_key(api_key)`: Get username from API key

## Database Operations

Database operations are performed using MySQL. Key functions include:

- `check_device_DB(deveui, password=None)`: Check device in database
- `add_device_DB(deveui, name, hashed_password)`: Add device to database
- `add_device_user_DB(deveui, username, superowner=0)`: Associate device with user
- `delete_device(deveui, username)`: Delete device from database

## API Endpoints

- `/api/deviceList`: Get list of user's devices
- `/api/deviceData/<deveui>`: Get data for a specific device
- `/api/publicDeviceData/<deveui>`: Get public data for a device
- `/api/registerDevice`: Register a new device
- `/api/deleteDevice`: Delete a device
- `/api/neighbourList/<deveui>`: Get list of neighboring devices
- `/api/getObject/<deveui>`: Get object data for a device

For more information see API documentation

## Utility Functions

- `hash_password(password)`: Hash password using bcrypt
- `check_password(hashed_password, user_password)`: Verify password
- `calculate_object_coordinates(emetteur_lat, emetteur_long, object_dist, object_x)`: Calculate object coordinates
- `add_data_to_cache(data)`: Add data to in-memory cache

This documentation provides an overview of the main components and functionalities of the Flask application. For more detailed information on each function or route, refer to the inline comments in the source code.

[retour à l'arborescence de la doc](../README.md)