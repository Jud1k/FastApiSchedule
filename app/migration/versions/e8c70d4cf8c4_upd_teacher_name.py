"""upd_teacher_name

Revision ID: e8c70d4cf8c4
Revises: ca63ef52f3ce
Create Date: 2025-04-24 15:04:56.045958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8c70d4cf8c4'
down_revision: Union[str, None] = 'ca63ef52f3ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "schedulelessons_room_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.drop_constraint(
        "schedulelessons_group_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.drop_constraint(
        "schedulelessons_teacher_id_fkey", "schedulelessons", type_="foreignkey"
    )
    op.drop_constraint(
        "schedulelessons_subject_id_fkey", "schedulelessons", type_="foreignkey"
    )

    # 1. Добавляем новую колонку как nullable
    op.add_column("teachers", sa.Column("name", sa.String(), nullable=True))

    # 2. Заполняем её данными
    op.execute("UPDATE teachers SET name = first_name || ' ' || last_name")

    # 3. Делаем колонку NOT NULL
    op.alter_column("teachers", "name", nullable=False)

    # 4. Добавляем уникальное ограничение
    op.create_unique_constraint(None, "teachers", ["name"])

    # 5. Удаляем старые колонки
    op.drop_column("teachers", "first_name")
    op.drop_column("teachers", "last_name")

    # Восстанавливаем foreign keys
    op.create_foreign_key(None, "schedulelessons", "groups", ["group_id"], ["id"])
    op.create_foreign_key(None, "schedulelessons", "teachers", ["teacher_id"], ["id"])
    op.create_foreign_key(None, "schedulelessons", "subjects", ["subject_id"], ["id"])
    op.create_foreign_key(None, "schedulelessons", "rooms", ["room_id"], ["id"])
    op.drop_constraint("students_group_id_fkey", "students", type_="foreignkey")
    op.create_foreign_key(None, "students", "groups", ["group_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "students", type_="foreignkey")
    op.create_foreign_key(
        "students_group_id_fkey",
        "students",
        "groups",
        ["group_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Восстанавливаем старые колонки
    op.add_column(
        "teachers",
        sa.Column("last_name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "teachers",
        sa.Column("first_name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )

    # Заполняем их из name
    op.execute(
        """
        UPDATE teachers 
        SET 
            first_name = split_part(name, ' ', 1),
            last_name = split_part(name, ' ', 2)
    """
    )

    # Удаляем новую колонку и ограничения
    op.drop_constraint(None, "teachers", type_="unique")
    op.drop_column("teachers", "name")

    # Восстанавливаем старые foreign keys
    op.drop_constraint(None, "schedulelessons", type_="foreignkey")
    op.drop_constraint(None, "schedulelessons", type_="foreignkey")
    op.drop_constraint(None, "schedulelessons", type_="foreignkey")
    op.drop_constraint(None, "schedulelessons", type_="foreignkey")
    op.create_foreign_key(
        "schedulelessons_subject_id_fkey",
        "schedulelessons",
        "subjects",
        ["subject_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "schedulelessons_teacher_id_fkey",
        "schedulelessons",
        "teachers",
        ["teacher_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "schedulelessons_group_id_fkey",
        "schedulelessons",
        "groups",
        ["group_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "schedulelessons_room_id_fkey",
        "schedulelessons",
        "rooms",
        ["room_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###
