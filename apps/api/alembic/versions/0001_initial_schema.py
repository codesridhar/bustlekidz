"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-13 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── users ──────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=True),
        sa.Column(
            "role",
            sa.Enum(
                "super_admin", "admin", "principal",
                "class_teacher", "teacher", "parent",
                name="userrole",
            ),
            nullable=False,
            server_default="parent",
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # ── classes ────────────────────────────────────────────────────────────
    op.create_table(
        "classes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("code", sa.String(20), nullable=False),
        sa.Column("age_min_months", sa.Integer(), nullable=False),
        sa.Column("age_max_months", sa.Integer(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False, server_default="25"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_classes_code"),
    )

    # ── sections ───────────────────────────────────────────────────────────
    op.create_table(
        "sections",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(10), nullable=False),
        sa.Column("class_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── students ───────────────────────────────────────────────────────────
    op.create_table(
        "students",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("admission_number", sa.String(50), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", sa.String(10), nullable=False),
        sa.Column("photo_url", sa.String(500), nullable=True),
        sa.Column("aadhaar_number", sa.String(12), nullable=True),
        sa.Column("blood_group", sa.String(5), nullable=True),
        sa.Column("allergies", sa.Text(), nullable=True),
        sa.Column("medical_notes", sa.Text(), nullable=True),
        sa.Column("class_id", sa.String(), nullable=True),
        sa.Column("section_id", sa.String(), nullable=True),
        sa.Column("door_no", sa.String(50), nullable=True),
        sa.Column("street", sa.String(255), nullable=True),
        sa.Column("area", sa.String(255), nullable=True),
        sa.Column("city", sa.String(100), nullable=False, server_default="Chennai"),
        sa.Column("pincode", sa.String(6), nullable=True),
        sa.Column("state", sa.String(100), nullable=False, server_default="Tamil Nadu"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["section_id"], ["sections.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("admission_number", name="uq_students_admission_number"),
    )
    op.create_index("ix_students_admission_number", "students", ["admission_number"], unique=True)

    # ── parents ────────────────────────────────────────────────────────────
    op.create_table(
        "parents",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("student_id", sa.String(), nullable=False),
        sa.Column("relation", sa.String(50), nullable=False, server_default="Father"),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(15), nullable=False),
        sa.Column("whatsapp_number", sa.String(15), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("occupation", sa.String(100), nullable=True),
        sa.Column("preferred_language", sa.String(10), nullable=False, server_default="en"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", name="uq_parents_user_id"),
    )
    op.create_index("ix_parents_student_id", "parents", ["student_id"])

    # ── teachers ───────────────────────────────────────────────────────────
    op.create_table(
        "teachers",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("employee_id", sa.String(50), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(15), nullable=False),
        sa.Column("qualification", sa.String(255), nullable=True),
        sa.Column("specialisation", sa.String(255), nullable=True),
        sa.Column("date_of_joining", sa.Date(), nullable=True),
        sa.Column("is_class_teacher", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("assigned_class_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["assigned_class_id"], ["classes.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", name="uq_teachers_user_id"),
        sa.UniqueConstraint("employee_id", name="uq_teachers_employee_id"),
    )

    # ── attendance_records ─────────────────────────────────────────────────
    op.create_table(
        "attendance_records",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("student_id", sa.String(), nullable=False),
        sa.Column("class_id", sa.String(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "present", "absent", "late", "half_day", "holiday",
                name="attendancestatus",
            ),
            nullable=False,
        ),
        sa.Column("marked_by", sa.String(), nullable=False),
        sa.Column("remarks", sa.String(255), nullable=True),
        sa.Column("whatsapp_sent", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["marked_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_attendance_student_date", "attendance_records", ["student_id", "date"])
    op.create_index("ix_attendance_class_date", "attendance_records", ["class_id", "date"])

    # ── enquiries ──────────────────────────────────────────────────────────
    op.create_table(
        "enquiries",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("parent_name", sa.String(255), nullable=False),
        sa.Column("child_name", sa.String(255), nullable=False),
        sa.Column("child_age_months", sa.Integer(), nullable=True),
        sa.Column("program_interest", sa.String(50), nullable=False),
        sa.Column("phone", sa.String(15), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("whatsapp_number", sa.String(15), nullable=True),
        sa.Column("source", sa.String(50), nullable=False, server_default="website"),
        sa.Column(
            "status",
            sa.Enum(
                "new", "visit_scheduled", "visit_done", "admission", "dropped",
                name="enquirystatus",
            ),
            nullable=False,
            server_default="new",
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("follow_up_date", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_enquiries_phone", "enquiries", ["phone"])
    op.create_index("ix_enquiries_status", "enquiries", ["status"])

    # ── seed: default classes ──────────────────────────────────────────────
    op.execute("""
        INSERT INTO classes (id, name, code, age_min_months, age_max_months, capacity) VALUES
        ('cls-pg',  'Playgroup', 'PG',  18, 36, 20),
        ('cls-dc',  'Daycare',   'DC',  12, 72, 15),
        ('cls-lkg', 'LKG',       'LKG', 48, 60, 25),
        ('cls-ukg', 'UKG',       'UKG', 60, 72, 25)
    """)

    op.execute("""
        INSERT INTO sections (id, name, class_id) VALUES
        ('sec-pg-a',  'A', 'cls-pg'),
        ('sec-dc-a',  'A', 'cls-dc'),
        ('sec-lkg-a', 'A', 'cls-lkg'),
        ('sec-ukg-a', 'A', 'cls-ukg')
    """)


def downgrade() -> None:
    op.drop_table("enquiries")
    op.drop_table("attendance_records")
    op.drop_table("teachers")
    op.drop_table("parents")
    op.drop_table("students")
    op.drop_table("sections")
    op.drop_table("classes")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS attendancestatus")
    op.execute("DROP TYPE IF EXISTS enquirystatus")
