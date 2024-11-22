import pytest
import json


with open("../data/test_data.json", "r") as f:
    test_data = json.load(f)


@pytest.mark.parametrize("case", test_data["test_cases"])
def test_asana(page, case):

    page.locator(f'a[aria-label="{case["project"]}, Project"]').click()
    page.wait_for_load_state()
    page.is_visible("div.ChipWithIcon--withChipFill")

    column = page.locator("div.CommentOnlyBoardColumn", has_text=case["column"])
    column.wait_for()

    task = column.locator("div.CommentOnlyBoardColumnCardsContainer-itemContainer", has_text=case["task"])
    task.wait_for()

    page.wait_for_timeout(500)
    tags = "".join(task.all_inner_texts())

    for tag in case["tags"]:
        assert tag in tags, f"Tag '{tag}' not found"
