-- Note: This schema was written for PostgreSQL and ported to SQLite.
-- The changes were: 
-- 1. SERIAL --> INTEGER PRIMARY KEY AUTOINCREMENT 
-- 2. DECIMAL --> REAL
-- 3. TIMESTAMP --> TEXT
-- 4. VARCHAR --> TEXT
-- 5. BOOLEAN --> INTEGER (1 for true, 0 for false)
-- 6. DEFAULT CURRENT_TIMESTAMP removed, handled by datetime.now().isoformat() in app's python code

CREATE TABLE IF NOT EXISTS year_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('STUDENT', 'TEACHER', 'ADMIN')),
    year_group_id INTEGER REFERENCES year_groups(id) ON DELETE SET NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS activation_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_hash TEXT NOT NULL UNIQUE,
    role_to_assign TEXT NOT NULL CHECK (role_to_assign IN ('STUDENT', 'TEACHER', 'ADMIN')),
    year_group_id INTEGER REFERENCES year_groups(id) ON DELETE SET NULL,
    created_by_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT,
    expires_at TEXT NOT NULL,
    is_used INTEGER NOT NULL DEFAULT 0,
    used_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    used_at TEXT
);

CREATE TABLE IF NOT EXISTS classrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    teacher_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT,
    is_published INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classroom_id INTEGER NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TEXT,
    CONSTRAINT unique_classroom_student UNIQUE (classroom_id, student_id)
);

CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classroom_id INTEGER NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('GENERAL', 'ESSAY', 'PROBLEMSET', 'PROJECT')),
    title TEXT NOT NULL,
    description TEXT,
    deadline TEXT NOT NULL,
    effort_hours REAL,
    difficulty INTEGER CHECK (difficulty BETWEEN 1 AND 5),
    is_published INTEGER NOT NULL DEFAULT 0,
    created_at TEXT,
    word_limit INTEGER,               -- ESSAY only
    number_of_problems INTEGER,       -- PROBLEMSET only
    min_group_size INTEGER,           -- PROJECT only
    max_group_size INTEGER            -- PROJECT only
);

CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classroom_id INTEGER NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    uploaded_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    uploaded_at TEXT
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assignment_id INTEGER NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    submitted_at TEXT,
    version INTEGER NOT NULL DEFAULT 1,
    feedback TEXT,
    CONSTRAINT unique_student_assignment_version UNIQUE (student_id, assignment_id, version)
);

CREATE TABLE IF NOT EXISTS attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL CHECK (kind IN ('FILE', 'LINK')),
    material_id INTEGER REFERENCES materials(id) ON DELETE CASCADE,
    submission_id INTEGER REFERENCES submissions(id) ON DELETE CASCADE,
    stored_filename TEXT,   -- FILE only
    original_filename TEXT, -- FILE only
    mime_type TEXT,         -- FILE only
    file_size_kb INTEGER,   -- FILE only
    url TEXT,               -- LINK only
    link_text TEXT,        -- LINK only
    uploaded_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    uploaded_at TEXT,
    -- XOR: attached to either a material OR a submission, never both or neither
    CONSTRAINT attachment_target_xor CHECK (
        (material_id IS NOT NULL AND submission_id IS NULL) OR
        (material_id IS NULL AND submission_id IS NOT NULL)
    )
);

CREATE TABLE IF NOT EXISTS progress_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assignment_id INTEGER NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'NEEDS_HELP')),
    status_changed_at TEXT,
    notes TEXT,
    CONSTRAINT unique_student_assignment UNIQUE (student_id, assignment_id)
);

CREATE TABLE IF NOT EXISTS help_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assignment_id INTEGER NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    created_at TEXT,
    is_urgent INTEGER NOT NULL DEFAULT 0,
    resolved_at TEXT,
    resolved_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    resolution_notes TEXT
);
