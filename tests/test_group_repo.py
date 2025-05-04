import pytest
from app.repositories.repository import GroupRepository
from sqlalchemy.exc import IntegrityError


@pytest.mark.asyncio
async def test_create_get(db):
    repo = GroupRepository(db)

    # Test create
    group = await repo.create({"name": "Group 1"})
    assert group.id is not None
    assert group.name == "Group 1"

    # Test get by id
    fetched = await repo.get_one_or_none_by_id(group.id)
    assert fetched.id == group.id
    assert fetched.name == group.name


@pytest.mark.asyncio
async def test_create_get_all(db):
    repo = GroupRepository(db)
    await repo.create({"name": "Group 1"})
    groups = await repo.get_all()
    assert len(groups) > 0
    assert any(g.name == "Group 1" for g in groups)


@pytest.mark.asyncio
async def test_create_with_duplicates(db):
    repo = GroupRepository(db)
    await repo.create({"name": "Group1"})
    with pytest.raises(IntegrityError):
        await repo.create({"name": "Group1"})


@pytest.mark.asyncio
async def test_create_delete(db):
    repo = GroupRepository(db)
    group_in = await repo.create({"name": "Group1"})
    await repo.delete(group_in.id)
    group = await repo.get_one_or_none_by_id(group_in.id)
    assert group is None


@pytest.mark.asyncio
async def test_create_update(db):
    repo = GroupRepository(db)
    group_in = await repo.create({"name": "Group1"})
    update_data = {"name": "Update Group1"}
    upd_group = await repo.update(group_in, update_data)
    assert group_in.id == upd_group.id
    assert upd_group.name == "Update Group1"


@pytest.mark.asyncio
async def test_update_with_duplicates(db):
    repo = GroupRepository(db)
    await repo.create({"name": "Group1"})
    group_in = await repo.create({"name": "Group2"})
    update_data = {"name": "Group1"}
    with pytest.raises(IntegrityError):
        await repo.update(group_in, update_data)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search_term,expected_count",
    [("Gr", 3), ("Group1", 1), ("unknown", 0), ("", 3)],
)
async def test_search_by_name(db, search_term, expected_count):
    repo = GroupRepository(db)
    await repo.create_many(
        [
            {"name": "Group1"},
            {"name": "group2"},
            {"name": "Another Group3"},
        ]
    )
    result = await repo.search(search_term)
    assert len(result) == expected_count
