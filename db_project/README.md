# Community Platform README

## Overview

This project is a web-based user interface for a local community platform, facilitating interactions between residents of specific neighborhoods and blocks. It allows users to register, log in, create and edit profiles, post messages, reply to threads, and engage in discussions within their designated blocks or neighborhoods.

## Getting Started

copy the .env.template file to .env and fill in the GOOGLE_API_KEY to get started. The API key should have permissions for google maps geocoding.

## Technical Specifications

- Backend Framework: Django
- Database System: PostgreSQL
- Web Server: Local machine setup
- Security Measures: Prepared statements, input sanitization, output encoding
- Documentation: A comprehensive report detailing architectural decisions, security measures, user guide, etc., will be submitted on Gradescope.

## TODO List

### Backend

1. **User Registration and Authentication**

   - [x] Implement registration functionality.
   - [x] Implement login functionality.
   - [x] Change legacy SQL authentication to DRF JWT authentication

2. **Profile Management**

   - [x] Create functionality for creating and editing profiles.
   - [x] Remove legacy SQL queries and implement Django ORM

3. **Communication and Interaction**

   - [x] Implement posting messages functionality.
   - [x] Implement replying to threads functionality.

4. **Information Display and Updates**

   - [ ] Develop main feed page showing recent threads.
   - [ ] Implement options to view threads with new messages.
   - [ ] Display profiles of newly joined members.

5. **Notifications**

   - [x] Create notification signals for friend requests creation
   - [x] Create notification signals for friend acceptance
   - [x] Create notification signals for a new follower
   - [ ] Create notfication for a new message in a thread that the user is a participant
   - [ ] Create notification for a new tag in a message

6. **Navigation and Search Functions**

   - [ ] Implement search functionalities based on keywords.
   - [ ] Implement search functionalities based on geographical proximity.
   - [ ] Implement ability to follow blocks for read-only access.

7. **Data Visualization (Optional)**
   - [ ] Explore and incorporate visual representations of data.

### Frontend

1. **User Registration and Authentication**
   - [ ] Design and implement registration form.
   - [ ] Design and implement login form.
2. **Profile Management**
   - [ ] Create profile creation and editing forms.
3. **Communication and Interaction**
   - [ ] Design and implement UI for posting messages.
   - [ ] Design and implement UI for replying to threads.
   - [ ] Design and implement UI for applying to join a block.
4. **Information Display and Updates**

   - [ ] Design main feed page.
   - [ ] Design UI for viewing threads with new messages.
   - [ ] Design UI for displaying profiles of newly joined members.

5. **Navigation and Search Functions**
   - [ ] Design UI for search functionalities.
   - [ ] Design UI for following blocks for read-only access.
6. **Data Visualization (Optional)**
   - [ ] Explore and design visual representations of data.

### Infrastructure

1. **Docker**
   - [x] Create docker-compose implementation for backend
   - [ ] Create docker-compose implementation for backend
2. **Observability**
   - [ ] Create observability stack using Prometheus and Grafana in docker-compose
3. **Cloud**
   - [ ] Create cloud docker implementations for services
   - [ ] Create Terraform for cloud deployment
4. **Performance**
   - [ ] Create performance tests using LocustIO to test user flows
   - [ ] Create dashboard for users to run performance tests and view results.
   - [ ] Limit number of users/threads a user can use for running performance tests so as not to overload the system

## Additional Notes

- Ensure to adhere to the functional requirements and technical specifications provided in the project description.
- Regularly test the application to ensure proper functionality and security measures are implemented.
- Collaborate effectively with team members to ensure all aspects of the project are covered.
