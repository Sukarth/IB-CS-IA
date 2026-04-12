<h1 style="text-align: center;">IA Plan - Criterion B</h1>

**Status:** Planned (may change)

## Project Steps

### 1. Specification

1. [X] Identify a real world issue and brainstorm ideas
2. [x] Figure out whether the issue can be solved through reasonable programmatic methods
    1. If not, go back to 1.1
3. [x] Think about possible programmatic solutions to the problem and brainstorm features the software may have
4. [x] Write the proposal about the idea and get it reviewed.
5. [ ] Consider and apply supervisor's comments.
6. [ ] Think about and write the success criterion for the software. Get it reviewed and address comments.

### 2. Planning

1. [x] Think about how to structure plan (into phases, stages, steps)
2. [x] Research and choose appropriate programming languages, platforms (web, desktop, mobile), and tools for the project.
3. [x] Think and choose appropriate algorithms and data structures to implement the software's features and capabilities
4. [x] Research similar software and existing solutions to the problem. Think about your software's differenciation, unique selling points, and justify why it's necessary and/or better than existing solutions
5. [x] Think about, define and design the software's requirements, specifications, and capabilities, including core features, user roles and capabilities, and any other relevant details.
6. [x] Write down the key success criteria for the software
7. [x] Define the project steps, and write down all the tasks for each step along with checkboxes to keep track of progress. Break the project into development phases in a realistic order.
8. [x] Write down the development timeline for the project, with estimated hours and timeframes for each task.
9. [ ] Design the database structure and identify the main entities. Design the ERD for the database.
10. [ ] Plan the class structure for the OOP parts, identifying the main classes and their attributes and methods. Create UML class diagrams for the OOP design.
11. [ ] Think about the frontend UI/UX design. Create wireframes and mockups.
12. [ ] Think about and create a storyboard for the software, showing the user interface and user experience of the software.
13. [ ] Plan the implementation of the key algorithms and data structures, including pseudocode and complexity analysis.
14. [ ] Think about testing and evaluation methods for the software, including how to test each feature and how to evaluate the software against the success criteria. Include functional tests (against success criteria) and structural tests (testing algorithm correctness). Write down the testing and evaluation plan including the above mentioned information.
15. [ ] Get plan reviewed and address comments as necessary.
16. [ ] Update the plan if features are added, removed, or reduced later.

### 3. Development

1. [ ] Set up development environment (Flask, Python, SQLite, Git repository)
2. [ ] Initialize database schema based on ERD
3. [ ] Implement authentication: registration with activation key, login, session management
4. [ ] Implement role-based access control (admin, teacher, student page restrictions) and user management
5. [ ] Implement OOP class for assignment types (base Assignment class and subclasses)
6. [ ] Implement classroom CRUD (create, read, update, delete) operations
7. [ ] Implement assignment CRUD operations linked to classrooms and assignment classes
8. [ ] Implement file upload and content library (materials attached to assignments or classrooms)
9. [ ] Implement student progress tracking and work submission features
10. [ ] Implement Analytics Dashboard (Bubble Sort & Binary Search algorithms)
    - [ ] Implement display of completion rates and ranking of students (Bubble Sort)
    - [ ] Implement searchable student and assignment records (Binary Search)
11. [ ] Implement Help Request system (Queue, Priority Queue & Linked List ADTs)
    - [ ] Implement Priority Queue ADT for urgent help requests (ordered by days remaining)
    - [ ] Implement teacher help request resolution dashboard (dequeue, view, resolve)
12. [ ] Implement Study Schedule Generator (Priority Queue ADT & urgency algorithm)
    - [ ] Implement warning system for uncompletable assignments in schedule generator
13. [ ] (Extra) Implement discussion threads using Stack ADT
14. [ ] (Extra) Implement notifications panel using Stack ADT
15. [ ] Add finishing touches to frontend UI/UX design
16. [ ] Tidy up and refactor code to improve maintainability where necessary.

### 4. Testing

1. [ ] Test and evaluate product against the Success Criteria
    - [ ] Write test cases thar map to each item in the Success Criteria, and evaluate whether the software meets each criterion based on the test results.
    - [ ] Test each core feature individually
    - [ ] Evaluate the overall product against the Success Criteria
2. [ ] Conduct unit testing on custom algorithms (Bubble sort, Binary search, Scheduler)
    - [ ] Test the correctness of the algorithms with various inputs, including edge cases (e.g. empty queue, zero days remaining, no available study hours).
3. [ ] Conduct integration testing for all database interactions
4. [ ] Perform User Acceptance Testing (UAT) with peers/teacher to get feedback on usability.
5. [ ] Fix bugs found during testing.
6. [ ] Re-test after each major fix.
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
| | Implement `Assignment` OOP class hierarchy (base + 4 subclasses) | 2 | Weeks 8–9 (Jun 1–14) |
| | Implement assignment CRUD, file uploads, and content library | 3 | Weeks 9–10 (Jun 8–21) |
| | Implement student progress tracking and work submission | 3 | Weeks 10–11 (Jun 15–28) |
| **Phase 3: Algorithms & ADTs** | Implement help request system: **Queue ADT** + **Priority Queue ADT** (backed by **Linked List ADT**) | 4 | Weeks 12–14 (Jun 29 – Jul 19) |
| | Implement teacher help request resolution dashboard | 4 | Week 14 (Jul 13–19) |
| | Implement analytics dashboard: **Bubble Sort** + **Binary Search** | 5 | Weeks 15–17 (Jul 20 – Aug 9) |
| | Implement study schedule generator: urgency algorithm + **Priority Queue ADT** | 4 | Weeks 18–20 (Aug 10–30) |
| **Phase 4: Stretch Features** | *(Extra)* Implement discussion threads using **Stack ADT** | 4 | Weeks 21–22 (Aug 31 – Sep 13) |
| | *(Extra)* Implement notifications panel using **Stack ADT** | 4 | Weeks 23–24 (Sep 14–27) |
| **Phase 5: Testing & Finalization** | Unit test all custom algorithms with edge cases | 2 | Weeks 25–26 (Sep 28 – Oct 11) |
| | Test all features against success criteria; fix bugs | 7 | Weeks 27–28 (Oct 12–25) |
| | UI/UX polish and final code refactor | 4 | Week 29 (Oct 26 – Nov 1) |
| | Record demonstration video | 2 | Week 30 (Nov 2–8) |
| | Complete final documentation and evaluation write-up | 7 | Weeks 31–32 (Nov 9–22) |
| **Total** | | *80h* | **Weeks 1–32 (Apr–Nov 2026)** |


## System Storyboard

### Planned Screens

1. **Login / Registration Page**
   - Email and password login
   - Activation key registration

2. **Teacher Dashboard**
   - View classrooms
   - View analytics summary
   - View top help requests

5. **Analytics Page**
   - Student completion rankings
   - Assignment completion rankings
   - Search functionality

6. **Help Queue Page**
   - Standard queue
   - Priority queue
   - Request resolution tools

3. **Student Dashboard**
   - View classrooms
   - View due assignments

7. **Study Planner Page**
   - Input daily study hours
   - Generate plan
   - View warnings for overload

4. **Admin Dashboard**
   - User management
   - Classroom management
   - Analytics overview
   
5. **Classroom Page**
   - View assignments
   - View materials
   - Manage students (teachers)
   - Access discussion threads

4. **Assignment Page**
   - Assignment details
   - Attached files and links
   - Update progress and submit work (students)
   - Submission area
   - Help request option
   - Optional discussion thread


---