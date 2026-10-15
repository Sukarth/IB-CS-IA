<center>

### IB Computer Science Internal Assessment

This is the repo for my IB Computer Science Internal Assessment. It contains the code for my project, as well as any relevant documentation and resources.

---

# **Study Tracker**

An Assignment Management and Tracking Application

Study Tracker is a web application built for schools, where teachers manage classrooms and assignments, students track their progress and submit work, and the application generates a personalised study schedule for each student, while ranking the students' help requests so that teachers can answer the most urgent ones first.

</center>

## Documentation

- The proposal is at [docs/Proposal.md](docs/Proposal.md) and is kept as originally written.
- The success criteria are located in [docs/SuccessCriteria.md](docs/SuccessCriteria.md).
- The plan is located in [docs/Plan.md](docs/Plan.md).
- The system overview (UI, UML diagrams, ERD, algorithms and test plan) is located in [docs/SystemOverview.md](docs/SystemOverview.md).

## Features

- **Admin:** Admins can generate activation keys (which decide the role of a new user, and the year group of a new student), manage year groups, and activate or deactivate user accounts.
- **Teacher:** Teachers can create, publish and delete classrooms, enroll/unenroll students, and create assignments of four types (General, Essay, Problem Set and Project). They can also share materials with file and link attachments, give feedback on submitted work/assignments, view a assignment completion analytics page for each classroom, and resolve students' help requests, which are listed in order of priority.
- **Student:** Students can see their published, enrolled classrooms and assignments, submit assignments with files and links containing their work, update their progress/status and log hours spent, and send help requests (can be marked urgent). They also get an automatically generated 14-day study schedule, shown on a monthly calendar with warnings, which is based on the free hours per weekday and the procrastination factor they enter on the settings page.
- **Everyone:** Every user can change their name, email and password on their account page.

## Tech Stack

- Python 3.13 (the version used for development and testing)
- [Flask](https://flask.palletsprojects.com/) with [Jinja2](https://jinja.palletsprojects.com/) templates
- SQLite, through Python's built-in `sqlite3` module
- [bcrypt](https://pypi.org/project/bcrypt/) for password hashing
- [email-validator](https://pypi.org/project/email-validator/) for checking email addresses
- [filetype](https://pypi.org/project/filetype/) for checking the real type of uploaded files

The exact versions are pinned in `requirements.txt`.

## Setup and running

The commands below are for Windows PowerShell and are run from the root folder of the repository. On macOS or Linux, use `source .venv/bin/activate` instead of `.venv\Scripts\Activate.ps1`.

1. **Create and activate a virtual environment, then install the dependencies.**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   If PowerShell refuses to run `Activate.ps1`, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` first.

2. **Create the file `instance/config.py`.** 

   The application will not start without it, and it is not part of the repository because the `instance/` folder is ignored by git (it holds each machine's own configuration, database and uploads). The file only needs to contain a secret key, which is used to sign the session cookies used by Flask.

   ```python
   SECRET_KEY = "type a long random string here"
   ```

   A suitable random string can be generated with `python -c "import secrets; print(secrets.token_hex(32))"`. The secret key should be kept private and never committed.

3. **Create the first admin account.** 

   Nobody can register without an activation key and only an admin can create keys, so the first admin has to be created manually from a script. Run the script from the root folder of the repository like so:

   ```powershell
   python -m app.database.create_admin
   ```

   The script asks for a name, an email, and a password (+ password confirmation). The email must be a valid address (reserved domains such as `.test` are rejected, so use e.g. `admin@example.com`). The password must be at least 8 characters long, and have a digit, an uppercase letter, a lowercase letter and a special character. The script quits if an admin already exists.

4. **Start the application.**
   
   Run the following command from the root folder of the repository:

   ```powershell
   python run.py
   ```

   The application will start and is then available at http://127.0.0.1:5000. `run.py` starts Flask's development server in debug mode, which is only meant for running the project on a local machine.

The database is created & initialized automatically from `app/database/schema.sql` the first time the application (or the admin script) runs, so no manual database setup is needed. The database is stored in `instance/app.sqlite` and the uploaded files (for materials or submissions) are stored in `instance/uploads/`. To start again from an empty state, stop the server, delete both of them and repeat step 3.

### Quickly explore the application

1. Log in as the admin, and create a year group on the admin dashboard (a student activation key needs a year group).
2. Open the Activation Keys page and generate keys for teachers and students. The keys are shown only once, so they must be saved immediately.
3. Each new user registers on the Register page with a key, then logs in. The key decides their role.
4. A teacher creates a classroom, publishes it, enrols students and creates assignments. Students only see classrooms and assignments that are published by their teacher.

## Project structure

```text
app/
  __init__.py     application factory, upload and key limits, error pages
  adt/            custom data structures: linked list, queue, priority linked list and priority queue
  algorithms/     study schedule generator and the help request priority and queue
  database/       SQLite helpers, schema.sql, file upload handling and the create_admin script
  models/         the OOP classes (users, classrooms, assignments, etc.) which contain all the database access
  routes/         Flask blueprints: auth, main, admin, teacher, student and files
  security/       login and role checks
  static/         style.css and nav.js
  templates/      Jinja2 templates for all pages
docs/             proposal, success criteria, plan, system overview, UML diagrams, ERD and the UI storyboard
feedback/         supervisor feedback notes
ib-cs-ia-guide/   git submodule with the IA supervisor's guidance (not required for running the application)
instance/         local configuration, database and uploads (not committed)
tests/            reserved for the automated tests, which have not been added yet
run.py            starting the development server (in debug mode)
requirements.txt  the application's dependencies
```

## UML

This project uses [Mermaid](https://mermaid.js.org/) (.mmd) for diagram *content*, which is rendered, styled/organized, and exported using [draw.io](https://www.drawio.com/).

Roles of files in `docs/UML/ADT/`, `docs/UML/Core/` and `docs/ERD/`:

| file | role |
| --- | --- |
| `*.mmd` | Mermaid class diagram code (source) |
| `*.drawio` | styled and arranged diagram (source + layout) |
| `*.svg`, `*.png` | exported images |

A `.drawio` file is created once by importing the `.mmd` (**Arrange → Insert → Advanced → Mermaid**), then styled and arranged by hand. Re-importing regenerates the shapes and discards that layout, so the `.drawio` must be edited directly instead.

The `~tools` directory contains scripts and other tools to help with diagram management.

### Exporting diagrams

Exports use the draw.io desktop CLI, which can be installed on windows using:

```bash
winget install JGraph.Draw
```

**Note:** This installs to `%LOCALAPPDATA%\Programs\draw.io\draw.io.exe` and is not added to `PATH`, so the folder must be added to `PATH` or the binary must be called by its full path.

Then, the following PowerShell commands, run from the root folder of the repository, export all three diagrams to svg and png:

```powershell
$drawio = "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe"
foreach ($d in "docs/UML/Core/CoreUML", "docs/UML/ADT/ADTUML", "docs/ERD/ERD") {
    & $drawio -x -f svg --theme light -o "$d.svg" "$d.drawio"
    & $drawio -x -f png -s 1 --theme light -o "$d.png" "$d.drawio"
}
```

## Git Submodule

This project uses a submodule `ib-cs-ia-guide` by Jarmo Hurri, the IA supervisor, which contains templates and other resources. To clone this repository with the submodule, use the following command:

```bash
git clone --recurse-submodules https://github.com/sukarth/ib-cs-ia.git
```

If you have already cloned the repository without the submodule, you can initialize and update the submodule with the following commands:

```bash
git submodule update --init --recursive
```

To simply sync/pull the latest changes from the submodule, use:

```bash
git submodule update --remote --merge --recursive
```
**Note**: run this command from the root of the repository, not from within the submodule directory.

Or, you can navigate to the submodule directory and pull the latest changes:

```bash
cd ib-cs-ia-guide
git pull origin main
```
---

Built with ❤️ by [Sukarth](https://github.com/sukarth)