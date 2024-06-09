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
   - [ ] Implement registration functionality.
   - [ ] Implement login functionality.
   - [ ] Integrate SQL queries directly for authentication.
   
2. **Profile Management**
   - [x] Create functionality for creating and editing profiles.
   - [x] Ensure SQL queries are used for profile management.

3. **Communication and Interaction**
   - [x] Implement posting messages functionality.
   - [x] Implement replying to threads functionality.
   - [ ] Implement applying to join a block functionality.
   
4. **Information Display and Updates**
   - [x] Develop main feed page showing recent threads.
   - [x] Implement options to view threads with new messages.
   - [ ] Display profiles of newly joined members.

5. **Navigation and Search Functions**
   - [x] Implement search functionalities based on keywords.
   - [ ] Implement search functionalities based on geographical proximity.
   - [ ] Implement ability to follow blocks for read-only access.
   
6. **Data Visualization (Optional)**
   - [ ] Explore and incorporate visual representations of data.

### Frontend
1. **User Registration and Authentication**
   - [x] Design and implement registration form.
   - [x] Design and implement login form.
   
2. **Profile Management**
   - [x] Create profile creation and editing forms.
   
3. **Communication and Interaction**
   - [x] Design and implement UI for posting messages.
   - [x] Design and implement UI for replying to threads.
   - [ ] Design and implement UI for applying to join a block.
   
4. **Information Display and Updates**
   - [x] Design main feed page.
   - [x] Design UI for viewing threads with new messages.
   - [ ] Design UI for displaying profiles of newly joined members.

5. **Navigation and Search Functions**
   - [x] Design UI for search functionalities.
   - [x] Design UI for following blocks for read-only access.
   
6. **Data Visualization (Optional)**
   - [x] Explore and design visual representations of data.

## Additional Notes
- Ensure to adhere to the functional requirements and technical specifications provided in the project description.
- Regularly test the application to ensure proper functionality and security measures are implemented.
- Collaborate effectively with team members to ensure all aspects of the project are covered.
