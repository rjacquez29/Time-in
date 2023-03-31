# Time-in

#### Video Demo: https://youtu.be/DQeHZXnPPuQ

#### Description:

Clock-in is a web application designed for shift registration and time-off requests. The application leverages geolocation to ensure that users are within the perimeter of their assigned workplace when clocking in. Each user has a set of assigned store location coordinates to verify their location. The project was created as part of the CS50 course, and the developer aims to improve the program by adding new features and increasing its efficiency as they acquire new skills.

The application uses **Flask**, **Flask-sqlalchemy**, and **werkzeug** for password hashing and ***Postgres DB*** for data storage. The project was created to assist my brother in managing his business's employee shifts and from my own ten years of experience working in shift-based conditions in large-scale retail and restaurants.

The application has two types of accounts: ***Manager*** and ***Staff***. Managers are the only ones who can register new users. The Timesheet feature enables users to view all the shifts they have worked in the current month, query other months, and see the total hours worked for each shift. If a user is currently clocked in, the clock-out option will appear as "currently clocked in," and the effective time will only show up after the user clocks out.

The ***Time-off*** feature enables users to create time-off requests by specifying the start and end dates and the reason. If only the start date is provided, the end date will automatically be set to the same date to help the manager manage employee requests if they are unable to work on coming days. Users can modify or delete requests that haven't been approved or declined yet, edit the reason statement, and update the start and end dates. If a change is made, the timestamp will show the time and date when the request was modified.

The ***People feature*** shows all colleagues in the same store, their roles, and email addresses for contact purposes. The developer also added a profile photo option to help users familiarize themselves with their colleagues' names and faces.

The ***Admin button*** is only visible to managers, allowing them to approve or decline time-off requests, add store locations for geolocation purposes, and register new users by uploading their information and profile pictures.

The application uses **Postgres** as its database management system since it allows for frequent information updates that SQLite3 cannot provide. The database includes registers for users, stores, timesheets, and time-offs.

Overall, Clock-in is a comprehensive web application that provides managers with tools to manage employee shifts efficiently and assists staff in managing their time-off requests.
