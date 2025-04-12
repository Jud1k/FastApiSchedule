"""4. Delete relations

Revision ID: ca63ef52f3ce
Revises: e38e76876fcb
Create Date: 2025-04-07 18:07:07.521262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca63ef52f3ce'
down_revision: Union[str, None] = 'e38e76876fcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Обновляем внешние ключи для ScheduleLesson
    op.drop_constraint(
        "schedulelessons_subject_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.create_foreign_key(
        "schedulelessons_subject_id_fkey",
        "schedulelessons",
        "subjects",
        ["subject_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "schedulelessons_teacher_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.create_foreign_key(
        "schedulelessons_teacher_id_fkey",
        "schedulelessons",
        "teachers",
        ["teacher_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "schedulelessons_room_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.create_foreign_key(
        "schedulelessons_room_id_fkey",
        "schedulelessons",
        "rooms",
        ["room_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "schedulelessons_group_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.create_foreign_key(
        "schedulelessons_group_id_fkey",
        "schedulelessons",
        "groups",
        ["group_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Обновляем внешние ключи для Student
    op.drop_constraint("students_group_id_fkey", "students", type_="foreignkey")
    op.create_foreign_key(
        "students_group_id_fkey",
        "students",
        "groups",
        ["group_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade():
    # Возвращаем обратно стандартные внешние ключи без CASCADE
    op.drop_constraint(
        "schedulelessons_subject_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.create_foreign_key(
        "schedulelessons_subject_id_fkey",
        "schedulelessons",
        "subjects",
        ["subject_id"],
        ["id"],
    )

    op.drop_constraint(
        "schedulelessons_teacher_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.create_foreign_key(
        "schedulelessons_teacher_id_fkey",
        "schedulelessons",
        "teachers",
        ["teacher_id"],
        ["id"],
    )

    op.drop_constraint(
        "schedulelessons_room_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.create_foreign_key(
        "schedulelessons_room_id_fkey", "schedulelessons", "rooms", ["room_id"], ["id"]
    )

    op.drop_constraint(
        "schedulelessons_group_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.create_foreign_key(
        "schedulelessons_group_id_fkey",
        "schedulelessons",
        "groups",
        ["group_id"],
        ["id"],
    )

    op.drop_constraint("students_group_id_fkey", "students", type_="foreignkey")
    op.create_foreign_key(
        "students_group_id_fkey", "students", "groups", ["group_id"], ["id"]
    )
