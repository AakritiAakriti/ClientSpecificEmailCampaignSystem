import pymysql
import pandas as pd
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import os

host = 'MyHostname.us-east-2.rds.amazonaws.com'
port = 3306
user = 'MyUser'
password = 'MyPassword'
database = 'MyDatabaseName'


client_data = {
    'email_address1@gmail.com': {'id': 27},
    'email_address2@yahoo.com': {'id': 16}
    # Here I can add more clients and their data
}

def fetch_client_data(client_id):
    # Connection string
    host = 'MyHostname.us-east-2.rds.amazonaws.com'
    port = 3306
    user = 'MyUser'
    password = 'MyPassword'
    database = 'MyDatabaseName'
    # Establish the connection
    connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    cursor = connection.cursor()


    # Define your SQL query
    sql_query = f"""
    SELECT
        cc.name AS client_name,
        COUNT(rs.title) AS total_reviews
    FROM
        client_client cc
    LEFT JOIN
        review_submission rs ON cc.id = rs.client_id
    WHERE
        cc.id = {client_id} AND rs.stars is NOT NULL
    GROUP BY
        cc.id, cc.name;
    """


#About my MySQL database: The database consists of several tables. The tables being used here in this script are as follows:
  # client_client: This table consists of the client specific data such as their name. Every client is assigned an ID which is the primary key of this table.
  # review_submission: This table consists of all the reviews collected for all the clients. Every row consists of multiple columns such as review star rating, review title, review description, review ID and each row has a column with client ID. This is the parameter on which the JOIN has been made.


    # Execute the query and fetch the results
    cursor = connection.cursor()
    cursor.execute(sql_query)

    # Fetch the result
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return result  # Returns (client_name, total_reviews) tuple




def send_email(client_email, client_name, total_reviews):
    # Compose email content
    message = Mail(
        from_email='no_reply@wholescale.com',
        to_emails=client_email,
        subject=f'Monthly Review Report for {client_name}',
        html_content=f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Wholescale Monthly Report</title>
                <style type="text/css">
                    body {{font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 0; background-color: #f2f2f2;}}
                    .email-container {{max-width: 600px; margin: auto; background-color: #ffffff;}}
                    .email-header {{background-color: #139880; color: white; padding: 20px; text-align: center;}}
                    .email-content {{padding: 20px;}}
                    .email-content h2 {{color: #333; font-size: 22px; margin-top: 0;}}
                    .email-content p {{color: #666; font-size: 16px; line-height: 1.5;}}
                    .email-footer {{background-color: #eeeeee; color: #333; text-align: center; padding: 20px; font-size: 12px;}}
                    .stats-block {{margin-bottom: 20px;}}
                    .stats-block h3 {{color: #333; font-size: 18px; margin-bottom: 5px;}}
                    .orange {{color: #139880;}}
                    .bold {{font-weight: bold;}}
                </style>
            </head>
            <body>
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td align="center" bgcolor="#f2f2f2">
                            <div class="email-container">
                                <!-- Header -->
                                <div class="email-header">
                                    <h1>Wholescale</h1>
                                    <p>November Monthly Ratings & Reviews Stats</p>
                                </div>
                                
                                <!-- Content -->
                                <div class="email-content">
                                    <div class="stats-block">
                                        <h2>{total_reviews} <span class="orange">reviews</span></h2>
                                    </div>
                            
                                    <!-- Additional sections can be added here -->
                                </div>
                                
                                <!-- Footer -->
                                <div class="email-footer">
                                    <p>This is an automated message from Wholescale.</p>
                                    <p>Please do not reply to this email.</p>
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
        '''

        f'<p>Dear {client_name},<br>Total Reviews: {total_reviews}</p>'

    )

    # Send email using SendGrid API
    sg = SendGridAPIClient('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')
    response = sg.send(message)

    # Print the status of the email sending process
    print(f"Email sent to {client_name} ({client_email}): {response.status_code}")


# Iterate through clients and send emails
for client_email, data in client_data.items():
    specific_client_id = data['id']

    # Fetch client data using the SQL query
    client_data_result = fetch_client_data(specific_client_id)

    # If client_data_result is not None (meaning client exists), send the email
    if client_data_result:
        client_name, total_reviews = client_data_result
        send_email(client_email, client_name, total_reviews)
    else:
        print(f"Client with ID {specific_client_id} not found.")
