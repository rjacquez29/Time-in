# Time-in

#### Video Demo: https://youtu.be/DQeHZXnPPuQ

#### Description:

Clock-in is a timesheet for shift registration, and it also records time-off request from users.
it uses geolocation to assert that you're within the pirimeter of the assigned work place when the user clocks in.
each user has an assigned store location coordinates, to chek if the user is within the perimiter of the assigned store.
this is a web application to apply the knowledge i learned from the CS50 course.

I decided to make this app for my brother's bussiness, to help him manage employees shifts, and also from my 10 years of experience in shift working condition in Large-scale retail and in restaurants.
I intend to improve this program in the near future by adding new features, make it more efficient, as soon as i learn new technologies and improve my coding skills.

### technologies used:
- Flask
- Flask-sqlalchemy
- werkzeug for password hash
- Postgres DB

.........................................................................................................................

### How it works:

There are two type's of accounts:
- Manager
- Staff

New user registration can only be made by managers.

### Timesheet
Allows you to see all the shifts you've worked in the current month
it also allows you to query other months by selecting the prefered month
By clicking on a shift, you can see the total hours worked for that shift
if the user is currently clocked in, the clock out will apear "currently clocked in" and only after the user clocks out will the affective time will show.


### Time-off
Create a time-off request from a given date, it requires start date, end date and your reason.
    - if you only put the start date, it automaticaly saves the end date as the same date.
    this is to help the manager for mananging employees request if un able to work in comming days.
-The request can be modified or delete by clicking on the selected shift. this can be done only if the request hasn't been approved or declined yet.
    - you can modify the start date and end date
    - you can also edit the reason statement.
      - once a change has benn made, the time stamp will be replaced with the time and date when the request has been changed and indicated that this request has been modified.

### People
See all colligues in the same store with thier respective role and e-mail addresses to contact. I decided to add the profile photo so other colligues can be familiarized by the face and name of thier work mates.

### Admin
this button will only show if the account loged in is from a manager, to limit access to the staff.
 Manage time-off request from staff
    -  Allows manager to Approve or Decline a time-off request.
    -  requests are then segregated by the action made ont the tab.
 Add a store location for Geolocation purposes.
  managers can add store location so when registering a new user, the list of stores will show on the options available.
    - Store name is required
    - Coordinates are copied and pasted from Google maps by searching the address of the intended store.
 Register a new user by inserting the new user's information and upload profile picture.
....................................................................................................

## Database: Postgres

i decided to use postgress because i have to update often the informations in the databse which sqlite3 won't allow me to do.

#### Registers:
 - Users
    - Name
    - Lastname
    - Email address
    - Password hash
    - Profile photo file path
    - Assigned store ID
    - User's role

- Stores
    - Store name
    - Longitude
    - Latitude

- Timesheet
    - Date and time
    - Clock-in
    - Clock-out

- Time off
    - Timestamp
    - From date
    - To date
    - Reason
    - status
