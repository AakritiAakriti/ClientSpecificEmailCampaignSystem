# ClientSpecificEmailCampaignSystem
# Monthly Review Report Script

## Overview

This Python script generates and sends monthly review reports to specified clients using SendGrid for email delivery. The data for each client is fetched from a MySQL database, and a customizable HTML email is constructed and sent.

## Dependencies

- `pymysql`: For MySQL database connectivity.
- `pandas`: For data manipulation and handling.
- `sendgrid`: For sending emails via SendGrid.

## Setup

1. Install the required dependencies using:
   ```bash
   pip install pymysql pandas sendgrid

Configure MySQL and SendGrid credentials:

I used my own host, user, password, and database variables in the script with my MySQL database details which have been removed from the script for security purposes.
Also, I set the SendGrid API key in the SendGridAPIClient initialization.

Customize Client Data:
To send emails to more clients, add more clients and their data to the client_data dictionary. This can also be done by maintaining the same record of client names and their emails in a separate table in MySQL database and fetching the data from their using a SELECT SQL query and putting that data in every iteration in a variable.

Usage
The script is a python code.
The script will iterate through clients, fetch their data from the database, and send personalized monthly review reports via email.

Additional Notes
Ensuring that the MySQL server is accessible and the required database schema exists is important.

Contributors
Aakriti
