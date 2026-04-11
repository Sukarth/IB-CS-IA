                            ━━━━━━━━━━━━━━━━
                             CS IA PROPOSAL
                            ━━━━━━━━━━━━━━━━


Project title
═════════════

Homework assignment and tracking system

Problem description
═══════════════════

In our school, there is no automated system for assigning homework and tracking its completion. Currently teachers are using varying platforms and manual work, such as Microsoft OneNote, Opiq, Showbie, Managebac and paper handouts. Particularly, neither teachers nor students can effectively track completion of homework. This problem requires a purpose built digital solution, as the usage and management of paper is prone to error, apart from being cumbersome and time consuming.
               
The solution will allow teachers to assign homework, students to mark homework completion, and both teachers and students to track homework completion.

To my knowledge there is currently no software available that is refined and purpose built for this problem. Furthermore, privacy issues require a solution over which the school has full control.

This solution will be a significant improvement for both students and teachers in a number of ways. It will save time for both parties by getting rid of multiple different systems and/or pieces of paper. Students will have a single place to keep track of assigned homework and its completion, due to a unified system for all their courses. This system will thus provide teachers with knowledge of which problems have been easy and which hard, allowing for more effective lessons and guidance. Additionally, teachers will have overall course completion rates for all the students, which can be used for course assessment.

The software solution:
══════════════════════

A website that is a management app built specifically for schools and their ease of use (self hostable, distributable (backend (DB) + frontend), which is similar in concept to Managebac or Google Classroom, but not exactly the same.

Requirements/specifications/success criteria:
═════════════════════════════════════════════

It should have an admin portal, where the admin can manage all app functions for the school (assign roles, etc)

3 roles: teacher, student, admin

login/signup based on email address with verification

there should be different interface + functions for teachers and students

should be focused on maximum user usability even for those not knowing tech much, while also being visually appealing (modern UI design). Main theme color should be blue.

Key role specific requirements:
-------------------------------

teachers should be able to (add, edit, delete):
- create/edit/delete classrooms and add/remove students to them.
- assign homework, add materials, add comments, images, pdfs, documents (docs, slides, code, etc), links
- registry/content library, organization, tables, schedules, lesson plans, lesson notes, units, criterion
- view students' details, info, progress on assignments/work, etc
- view students' submitted work for assignments, add comments on work, and more

students should be able to:
- view all required info and materials
- add comments/questions in places (if allowed by teacher)
- have access to discussions or discussion threads (if allowed by teacher)
    - where teacher can also see and reply
- submit work to assignments, and/or mark their progress on assignments, and add comments/questions directly to the teacher
- allowed to mark and track their progress in different places, like assignments, any material added by teacher, units, etc (to act like a study tracker of what all they have learnt/studied and to what level/extent --> sort of like a todo list for themselves)
    - should also be visible to teacher
- should have access to a homepage with calendar, tasks, todo list (can add custom items & schedule/time/deadlines & labels/filters & notes, but also has items automatically added based on status (check previous point)(allow disabling/enabling feature)) and panel with (new) messages for them to check and an updates/notification area (ex: new assignment added by a teacher, etc), along with a system messages area (if admin wants to send any info/messages, etc like system maintenance times or other school wide events etc)

admins should be able to:
- configure and categorize students into 'years' or grades, so they can be better managed: 
  - ex scheduling system or general events for the whole group or sending a system message

Solution platform
═════════════════

Solution will be a website with a connection to a database server. This
is an appropriate platform, since the software can run and be used on a variety of devices such as phones, tablets, and laptops. The website and database server can be self-hosted by the school.