# Time-in | web application

#### Video Demo: https://youtu.be/DQeHZXnPPuQ

#### Introduction:

Welcome to the Clock-in web application documentation, designed for shift registration and time-off requests. This application was created as part of the Harvard University's CS50 - an introduction to computer science course and aims to assist managers in efficiently managing their employees' shifts while providing staff with tools to manage their time-off requests. 

#### System Architecture:

Clock-in is a Flask-based web application that leverages Flask-sqlalchemy and werkzeug for password hashing. The application uses Postgres as its database management system, which allows for frequent information updates. The database comprises registers for users, stores, timesheets, and time-offs.

#### Application Features:

1. **Geolocation-based clock-in**: The application leverages geolocation to ensure that users are within the perimeter of their assigned workplace when clocking in. Each user has a set of assigned store location coordinates to verify their location.

2. **User Accounts**: The application has two types of accounts: Manager and Staff. Managers are the only ones who can register new users.

3. **Timesheet feature**: The Timesheet feature enables users to view all the shifts they have worked in the current month, query other months, and see the total hours worked for each shift. If a user is currently clocked in, the clock-out option will appear as "currently clocked in," and the effective time will only show up after the user clocks out.

4. **Time-off feature**: The Time-off feature enables users to create time-off requests by specifying the start and end dates and the reason. If only the start date is provided, the end date will automatically be set to the same date to help the manager manage employee requests if they are unable to work on coming days. Users can modify or delete requests that haven't been approved or declined yet, edit the reason statement, and update the start and end dates. If a change is made, the timestamp will show the time and date when the request was modified.

5. **People feature**: The People feature shows all colleagues in the same store, their roles, and email addresses for contact purposes. The developer also added a profile photo option to help users familiarize themselves with their colleagues' names and faces.

6. **Admin feature**: The Admin button is only visible to managers, allowing them to approve or decline time-off requests, add store locations for geolocation purposes, and register new users by uploading their information and profile pictures.

#### Conclusion:

In conclusion, the Clock-in web application is a comprehensive tool for managers to efficiently manage their employees' shifts and for staff to manage their time-off requests. The application's features, including geolocation-based clock-in, user accounts, timesheet, time-off, people, and admin features, make it a comprehensive solution for businesses looking to improve their shift management processes. Additionally, one of the key advantages of the Clock-in web application is that it leverages the use of web technology, eliminating the need for users to download a separate app. This means that managers and staff can access the platform seamlessly through their web browsers on various devices, such as desktop computers, laptops, tablets, and smartphones, enhancing accessibility and user convenience. By adopting a web-based approach, the Clock-in application ensures that users can efficiently manage their shifts and time-off requests without the hassle of app installations, making it an even more practical and user-friendly solution for modern businesses.
