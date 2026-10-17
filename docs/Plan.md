<h1 style="text-align: center;">IA Plan - Criterion B</h1>

**Status:** Development complete. Testing and evaluation in progress

**Final program name chosen:** Study Tracker

## Project Steps

### 1. Specification

1. [X] Identify a real world issue and brainstorm ideas
2. [x] Figure out whether the issue can be solved through reasonable programmatic methods
    - If not, go back to 1.1
3. [x] Think about possible programmatic solutions to the problem and brainstorm features the software may have
4. [x] Write the proposal about the idea and get it reviewed.
5. [x] Consider and apply supervisor's comments.
6. [x] Think about and write the success criterion for the software. Get it reviewed and address comments.

### 2. Planning

1. [x] Think about how to structure plan (into phases, stages, steps)
2. [x] Research and choose appropriate programming languages, platforms (web, desktop, mobile), and tools for the project.
3. [x] Think and choose appropriate algorithms and data structures to implement the software's features and capabilities
4. [x] Research similar software and existing solutions to the problem. Think about your software's differenciation, unique selling points, and justify why it's necessary and/or better than existing solutions
5. [x] Think about, define and design the software's requirements, specifications, and capabilities, including core features, user roles and capabilities, and any other relevant details.
6. [x] Write down the key success criteria for the software
7. [x] Define the project steps, and write down all the tasks for each step along with checkboxes to keep track of progress. Break the project into development phases in a realistic order.
8. [x] Write down the development timeline for the project, with estimated hours and timeframes for each task.
9. [x] Design the database structure and identify the main entities. Design the ERD for the database.
10. [x] Plan the class structure for the OOP parts, identifying the main classes and their attributes and methods. Create UML class diagrams for the OOP design.
11. [x] Think about the frontend UI/UX design. Create wireframes and mockups.
12. [x] Think about and create a storyboard for the software, showing the user interface and user experience of the software.
13. [ ] Plan the implementation of the key algorithms and data structures, including pseudocode and complexity analysis.
14. [ ] Think about testing and evaluation methods for the software, including how to test each feature and how to evaluate the software against the success criteria. Include functional tests (against success criteria) and structural tests (testing algorithm correctness). Write down the testing and evaluation plan including the above mentioned information.
15. [x] Get plan reviewed and address comments as necessary.
16. [x] Update the plan if features are added, removed, or reduced later.

### 3. Development

1. [x] Set up development environment (Flask, Python, SQLite, Git repository)
2. [x] Initialize database schema based on ERD
3. [x] Implement authentication: registration with activation key, login, session management
4. [x] Implement role-based access control (admin, teacher, student page restrictions) and user management
5. [x] Implement OOP class for assignment types (base Assignment class and subclasses)
6. [x] Implement classroom CRUD (create, read, update, delete) operations
7. [x] Implement assignment CRUD operations linked to classrooms and assignment classes
8. [x] Implement file upload and content library (attach files and links to materials and submissions)
9. [x] Implement student progress tracking and work submission features
10. [x] Implement Analytics Dashboard
    - [x] Implement ranking of students
    - [x] Implement searchable student and assignment records
11. [x] Implement Help Request system (Priority Queue & Priority Linked List ADTs)
    - [x] Implement Priority Queue ADT for help requests
    - [x] Implement teacher help request resolution dashboard (view, resolve)
12. [x] Implement Study Schedule Generator (custom algorithm)
    - [x] Implement warning system for uncompletable assignments in schedule generator
13. [ ] Add finishing touches to frontend UI/UX design
14. [x] Think of the final name for the program
15. [x] Tidy up and refactor code to improve maintainability where necessary.

### 4. Testing

1. [ ] Test and evaluate product against the Success Criteria
    - [ ] Write test cases that map to each item in the Success Criteria, and evaluate whether the software meets each criterion based on the test results.
    - [ ] Test each core feature individually
    - [ ] Evaluate the overall product against the Success Criteria
2. [ ] Unit test the custom scheduling algorithm, the help request priority calculation, and the data structures
    - [ ] Test correctness with various inputs, including edge cases (e.g. empty queue, zero days remaining, no available study hours).
3. [ ] Conduct integration testing for all database interactions
4. [ ] Perform User Acceptance Testing (UAT) with peers/teacher to get feedback on usability.
5. [x] Fix bugs found during testing.
6. [x] Re-test after each major fix.
7. [ ] Record evidence of successful tests for documentation and video.

### 5. Evaluation and Finalization

1. [ ] Evaluate and assess the finished product against each success criterion.
    - [ ] For each criterion, write down whether the software meets it or not based on the testing results, and provide evidence from the tests to support the evaluation.
2. [ ] Identify realistic limitations and possible future improvements.
3. [ ] Gather screenshots, diagrams, code excerpts and other materials for the final document.
4. [ ] Record the demonstration video (5 minutes) showing the product's functionality
    - [ ] Carefully and clearly walk through each of the success criteria. Explain how the software meets each criterion through the demonstration of features and using evidence from testing where applicable.
5. [ ] Complete the final IA documentation and appendix.
6. [ ] Submit the draft version and get feedback from the supervisor.
7. [ ] Address any comments and feedback from the supervisor, making necessary improvements to the product and documentation.
8. [ ] Submit the final version.

---

## Development Timeline

| Phase | Task | Hours | Timeframe |
|---|---|---|---|
| **Phase 0: Specification & Planning** | Finalize proposal and success criteria after supervisor feedback | 2 | Weeks 1–2 (Apr 13–26) |
| | Design database ERD and OOP UML class diagrams | 3 | Weeks 2–3 (Apr 20 – May 3) |
| | Create wireframes, storyboard, and system overview | 4 | Week 3 (Apr 27 – May 3) |
| | Write pseudocode and complexity notes for key algorithms | 2 | Week 3 (Apr 27 – May 3) |
| | Write testing and evaluation plan | 3 | Week 4 (May 4–10) |
| **Phase 1: Environment Setup** | Set up Flask project, Git repository, and SQLite | 0.5 | Week 4 (May 4–10) |
| | Initialise database schema from ERD | 0.5 | Week 5 (May 11–17) |
| **Phase 2: Core Infrastructure** | Implement authentication: activation keys, registration, login, sessions | 5 | Weeks 5–6 (May 11–24) |
| | Implement role-based access control and admin user management | 1 | Week 7 (May 25–31) |
| | Implement classroom CRUD and student enrollment | 4 | Weeks 7–8 (May 25 – Jun 7) |
| | Implement `Assignment` OOP class hierarchy (base + subclasses) | 2 | Weeks 8–9 (Jun 1–14) |
| | Implement assignment CRUD, file uploads, and content library | 3 | Weeks 9–10 (Jun 8–21) |
| | Implement student progress tracking and work submission | 3 | Weeks 10–11 (Jun 15–28) |
| **Phase 3: Algorithms & ADTs** | Implement help request system: **Priority Queue ADT** (backed by **Priority Linked List ADT**) | 4 | Weeks 12–14 (Jun 29 – Jul 19) |
| | Implement teacher help request resolution dashboard | 4 | Week 14-15 (Jul 13–26) |
| | Implement analytics dashboard | 5 | Weeks 16–19 (Jul 27 – Aug 23) |
| | Implement study schedule generator: custom algorithm + **Priority Queue ADT** | 4 | Weeks 20–24 (Aug 24 – Sep 27) |
| **Phase 4: Testing & Finalization** | Unit test all custom algorithms with edge cases | 2 | Weeks 25–26 (Sep 28 – Oct 11) |
| | Test all features against success criteria; fix bugs | 7 | Weeks 27–28 (Oct 12–25) |
| | UI/UX polish and final code refactor | 4 | Week 29 (Oct 26 – Nov 1) |
| | Record demonstration video | 2 | Week 30 (Nov 2–8) |
| | Complete final documentation and evaluation write-up | 7 | Weeks 31–32 (Nov 9–22) |
| **Total** | | *72h* | **Weeks 1–32 (Apr–Nov 2026)** |


## System Storyboard

### Planned Screens

1. **Login / Registration Page**
    - Email and password login
    - Activation key registration

2. **Teacher Dashboard**
    - View classrooms
    - View top help requests

3. **Analytics Page**
    - Student completion rankings
    - Assignment completion rankings
    - Search functionality

4. **Help Queue shown on teacher dashboard**
    - Priority queue
    - Request resolution

5. **Student Dashboard**
    - View classrooms
    - View due assignments

6. **Study Schedule Page**
    - View generated schedule
    - View warnings for uncompletable/unscheduled assignments

7. **Study Schedule Settings Page**
    - Input available study hours
    - Input procrastination factor
    - Exclude overdue assignments option

8. **Admin Dashboard**
    - User management
    - Activation key management

9. **Classroom Page**
    - View assignments
    - View materials
    - Manage students (teachers)

10. **Assignment Page**
    - Assignment details
    - Attached files and links in a student's submission (teachers)
    - Update progress and submit work (students)
    - Submission area
    - Help request option


---