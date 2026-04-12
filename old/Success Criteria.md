<h1 style="text-align: center;">Success Criteria</h1>

**Status:** Planned (may change)

## Success Criteria

1. **User Role Management**: An administrator can create and manage user roles, granting users either teacher or student roles.

2. **Authentication & Verification**: Users (teachers, students, admins) can register and login using email and password, with email verification required before access is granted.

3. **Classroom Management**: A teacher can create, edit, and delete classrooms, and add or remove students from them.

4. **Assignment Creation**: A teacher can create, edit, and delete assignments, attaching at least one of the following:
   - Text description
   - File (PDF, document, image, code)
   - External link

5. **Assignment Status Tracking**: A student can view all assignments in their enrolled classrooms and mark each as:
   - Not started
   - In progress
   - Completed
   - Needs help

6. **Assignment Completion Summary**: A teacher can view a summary of all students' completion statuses for any given assignment, showing counts per status category.

7. **Overall Completion Rate**: A student can view their own overall completion rate (as a percentage) across all assignments in a course.

8. **Content Library Management**: A teacher can create and manage a content library of materials (notes, files, links) organized by unit or topic, visible to enrolled students.

9. **Student Homepage Dashboard**: A student's homepage displays:
   - Calendar with upcoming assignment deadlines
   - Notification panel showing new assignments and teacher comments

10. **System-Wide Messaging**: An admin can send a system-wide message visible to all users:
    - Immediately if the user is logged in
    - Upon their next login if offline

11. **Data Persistence & Self-Hosting**: All user data is stored persistently in a database, and the application can be self-hosted by a school on their own server.

---

## Teacher Feedback & Questions

2. do we need multiple admins?
4. are assignments tied to specific classroom?
6. can teacher see percentages?
8. any kind of binary files?
11. persistent storage assumed, so can be removed; 11 perhaps not necessary overall

---
