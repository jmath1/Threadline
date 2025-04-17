# Community Platform README

## Overview

This project is a web-based user interface for a local community platform, facilitating interactions between residents of specific neighborhoods and blocks. It allows users to register, log in, create and edit profiles, post messages, reply to threads, and engage in discussions within their designated blocks or neighborhoods.

The platform leverages multiple databases and technologies to enhance performance and scalability, including PostgreSQL, MongoDB, Redis, and asynchronous task queues.

## Getting Started

Copy the `.env.template` file to `.env` and fill in the `GOOGLE_API_KEY` to get started. The API key should have permissions for Google Maps geocoding.

## Technical Specifications

- **Backend Framework**: Django
- **Database Systems**:
  - **PostgreSQL**: Used for relational data like user profiles, threads, and hood relationships.
  - **MongoDB**: Used for unstructured or semi-structured data such as messages, tags, and activity logs.
  - **Redis**: Used for real-time caching, notifications, and rate-limiting.
- **Task Queue**: Celery with Redis broker for handling asynchronous tasks like notifications and media processing.
- **Web Server**: Local machine setup
- **Security Measures**: Prepared statements, input sanitization, output encoding
- **Documentation**: A comprehensive report detailing architectural decisions, security measures, user guide, etc., will be submitted on Gradescope.

## TODO List

### Backend

1. **User Registration and Authentication**

   - [x] Implement registration functionality.
   - [x] Implement login functionality.
   - [x] Change legacy SQL authentication to DRF JWT authentication.

2. **Profile Management**

   - [x] Create functionality for creating and editing profiles.
   - [x] Remove legacy SQL queries and implement Django ORM.

3. **Communication and Interaction**

   - [x] Implement posting messages functionality.
   - [x] Implement replying to threads functionality.
   - [x] Restrict message creation to threads that are public, associated with the user's hood, or where the user is a participant.
   - [x] Restrict thread creation to hoods that are associated with the user.
   - [x] Restrict thread/message tagging to users that the author is friends with.

4. **Information Display and Updates**

   - [x] Develop main feed page showing recent threads.
   - [x] Implement options to view threads with new messages.
   - [x] Display profiles of newly joined members.

5. **Notifications**

   - [x] Create notification signals for friend requests creation.
   - [x] Create notification signals for friend acceptance.
   - [x] Create notification signals for a new follower.
   - [x] Create notifications for a new message in a thread that the user is a participant.
   - [x] Create notifications for a new tag in a message.
   - [ ] Notifications should be stored in Mongo and also have a pubsub channel in redis for new notifications while the user is logged in.

6. **Navigation and Search Functions**

   - [ ] Implement search functionalities based on keywords.
   - [ ] Implement search functionalities based on geographical proximity.
   - [ ] Implement ability to follow blocks for read-only access.

7. **Asynchronous Tasks**

   - [ ] Implement background tasks for notifications using Celery.
   - [ ] Implement asynchronous media processing for image and video uploads.

8. **Data Visualization (Optional)**
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

   - [x] Create docker-compose implementation for backend.
   - [ ] Create docker-compose implementation for frontend.

2. **Database**

   - [ ] Create docker-compose implementation for PostgreSQL.
   - [ ] Create docker-compose implementation for MongoDB.

3. **Redis**

   - [ ] Implement Redis for caching, notifications, and rate-limiting.

4. **Observability**

   - [ ] Create observability stack using Prometheus and Grafana in docker-compose.

5. **Cloud**

   - [ ] Create cloud docker implementations for services.
   - [ ] Create Terraform for cloud deployment.

6. **Performance**
   - [ ] Create performance tests using LocustIO to test user flows.
   - [ ] Create a dashboard for users to run performance tests and view results.
   - [ ] Limit the number of users/threads a user can include in performance tests to avoid overloading the system.
