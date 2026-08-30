<h1 style="text-align: center;">CS IA PROPOSAL</h1>

## Project Title

Assignment Management and Tracking System

---

## Problem Description

In our school, there is no automated system for assigning homework and tracking its completion. Currently, teachers use varying platforms and manual work, such as Microsoft OneNote, Opiq, Showbie, Managebac, and paper handouts. Specifically, neither teachers nor students can effectively track the completion of homework. This problem requires a purpose-built digital solution, as the usage and management of paper is prone to error, apart from being cumbersome and time-consuming.

The solution will allow:
- Teachers to assign homework
- Students to mark homework completion
- Both teachers and students to track homework completion

To the best of my knowledge, there is currently no refined, purpose-built software available for this problem. Furthermore, privacy concerns require a solution over which the school has full control.

Additionally, current solutions do not help students manage _when_ to work on assignments, only _what_ is due. This software solves this issue by generating personalised day-by-day study schedules based on each assignment's deadline and estimated effort. Platforms like Google Classroom offer basic assignment tracking, but none provide algorithmic study schedule generation based on deadline proximity and effort, nor do they allow schools to self-host their data under their own privacy policies.

## Benefits/Impact

This solution will be a significant improvement for both students and teachers in a number of ways. It will save time for both parties by getting rid of multiple different systems and/or pieces of paper. Students will have a single place to keep track of assigned homework and its completion, due to a unified system for all their courses. This system will thus provide teachers with knowledge of which problems have been easy and which hard, allowing for more effective lessons and guidance. Additionally, teachers will have overall course completion rates for all the students, which can be used for course assessment.

## Solution Platform

A web-based python application (website) consisting of both a backend (database) and frontend component for easy distribution and self-hosting by schools on their own servers.

This is an appropriate platform for this software due to its accessibility: users can access the system from any device with an internet connection (such as phones, tablets, and laptops), without needing to download and install an app. Additionally, the website and database server can be self-hosted by the school relatively easily, without needing to worry about app store distribution or compatibility with different operating systems (as with mobile or desktop apps).

---

## Detailed Requirements & Specifications

### Core Features

- **Admin Portal**: Administrators can manage all app functions for the school (assign roles, etc.)
- **Role-Based System**: Three roles available: teacher, student, and admin (^)
- **Authentication**: Login/signup based on email address with 1st time activation key
- **User Interface**: Different interfaces and functions for teachers and students, focused on maximum usability for non-technical users, while being visually appealing with a modern UI/UX design

### Teacher Capabilities

Teachers should be able to:

**Manage Classrooms**
- Create, edit, and delete classrooms that they own
- Add and remove students from classrooms

**Assign & Manage Materials**
- Assign homework
- Add materials, comments, documents (docs, images, PDFs, slides, code, etc.), and links (^)
- Manage content library, organization, tables, schedules, lesson plans, lesson notes, units, and criteria (^)

**Monitor Students**
- View student details, information, and progress on assignments/work (^)
- View students' submitted work for assignments
- Add comments on submitted work (TBD)

### Student Capabilities

Students should be able to:

**Access Materials**
- Access their classrooms and assignments
- View all required information and materials
- View details, information, and progress on assignments/work (^)
    - learned/studied content and level of mastery (TBD)

**Communicate**
- Access discussions or discussion threads (if allowed by teacher)
- Add comments/questions in allowed places (^)
- Add comments/questions directly to the teacher

**Track Progress**
- Submit work to assignments
- Mark and track progress in different places (assignments, study materials, units, etc.)

**Access Homepage Features**
- Calendar displaying upcoming deadlines
- Tasks and to-do list (customizable with schedule, time, deadlines, labels, filters, and notes) (TBD: will likely just be a simple task list containing all upcoming due homework/tasks) (^)
    - Automatic population of items based on assignment status (toggleable)
- Notification/updates panel for new messages or events (e.g., new assignment added by teacher) (^)

### Admin Capabilities

Administrators should be able to:

- Configure and categorize students into 'years' or grades for better management (^)
- Manage user accounts and roles (assigning teacher/student/admin roles, etc.) including activation key management (^)

---

Note: items marked with (^) represent potential opportunities to apply object-oriented programming principles in the implementation.

Some examples from above include:
- type of post: comment or question.
- type of content/material: document, link, image, etc.
- type of user: teacher, student, admin.
- type of assignment: essay, problem set, project, etc.
- type of task: homework, studying, project work, etc.
- type of notification: new assignment, new comment, etc.
- type of progress: not started, in progress, completed, etc.
- type of detail/information: assignment details, student details, etc.

- Stacks (ADT) can be used for discussion threads, comment threads, and notification history.

---
