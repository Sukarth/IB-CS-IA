<h1 style="text-align: center;">CS IA PROPOSAL</h1>

**Status:** Planned (may change)

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

## Benefits/Impact

This solution will be a significant improvement for both students and teachers in a number of ways. It will save time for both parties by getting rid of multiple different systems and/or pieces of paper. Students will have a single place to keep track of assigned homework and its completion, due to a unified system for all their courses. This system will thus provide teachers with knowledge of which problems have been easy and which hard, allowing for more effective lessons and guidance. Additionally, teachers will have overall course completion rates for all the students, which can be used for course assessment.

## Solution Platform

A self-hostable web-based application built specifically for schools, containing:
- Both backend (database) and frontend components for easy distribution
- Conceptual similarity to Managebac or Google Classroom, but purpose-built specifically for homework management
- Support for schools to self-host on their own servers

A web-based application (website) is an appropriate platform for this software due to its accessibility: users can access the system from any device with an internet connection (such as phones, tablets, and laptops), without needing to download and install an app. Additionally, the website and database server can be self-hosted by the school relatively easily, without needing to worry about app store distribution or compatibility with different operating systems (as with mobile or desktop apps).

---

## Requirements & Specifications

### Core Features

- **Admin Portal**: Administrators can manage all app functions for the school (assign roles, etc.)
- **Role-Based System**: Three roles available: teacher, student, and admin
- **Authentication**: Login/signup based on email address with email verification
- **User Interface**: Different interfaces and functions for teachers and students, focused on maximum usability for non-technical users, while being visually appealing with a modern UI/UX design

### Teacher Capabilities

Teachers should be able to:

**Manage Classrooms**
- Create, edit, and delete classrooms
- Add and remove students from classrooms

**Assign & Manage Materials**
- Assign homework
- Add materials, comments, images, PDFs, documents (docs, slides, code, etc.), and links
- Manage content library, organization, tables, schedules, lesson plans, lesson notes, units, and criteria

**Monitor Students**
- View student details, information, and progress on assignments/work
- View students' submitted work for assignments
- Add comments on submitted work

### Student Capabilities

Students should be able to:

**Access Materials**
- Access their classrooms and assignments
- View all required information and materials
- Add comments/questions in allowed places

**Communicate**
- Access discussions or discussion threads (if allowed by teacher)
- Submit work to assignments and/or mark progress on assignments
- Add comments/questions directly to the teacher

**Track Progress**
- Mark and track progress in different places (assignments, materials, units, etc.)
- Use the system as a personal study tracker for learned/studied content and level of mastery
- Use the system to manage tasks similar to a to-do list

**Access Homepage Features**
- Calendar displaying upcoming deadlines
- Tasks and to-do list (customizable with schedule, time, deadlines, labels, filters, and notes)
    - Automatic population of items based on assignment status (toggleable)
- Notification/updates panel for new messages or events (e.g., new assignment added by teacher)
- System messages area (admin announcements, maintenance notices, school-wide events)

### Admin Capabilities

Administrators should be able to:

- Configure and categorize students into 'years' or grades for better management
- Schedule system-wide events or announcements
- Send system messages to specific student groups
- Manage all organizational and user management functions

---
