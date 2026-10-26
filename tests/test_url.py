import pytest

from py_simple_package.src.py_simple import (
    get_path as public_get_path,
)
from py_simple_package.src.py_simple.easy_url import (
    EasyUrlError,
    add_query_param,
    get_domain,
    get_path,
    is_https,
    remove_query_param,
)


def test_get_domain():
    assert get_domain("https://school.example/clubs") == "school.example"


def test_is_https():
    assert is_https("https://school.example") is True
    assert is_https("http://school.example") is False


def test_add_query_param_sets_and_replaces():
    start = "https://school.example/clubs"
    with_page = add_query_param(start, "page", "2")
    assert with_page == "https://school.example/clubs?page=2"
    assert (
        add_query_param(with_page, "page", "3") == "https://school.example/clubs?page=3"
    )


def test_get_path():
    assert get_path("https://school.example/clubs/art") == "/clubs/art"
    assert get_path("https://school.example/") == "/"
    assert get_path("https://school.example") == "/"
    assert get_path("https://school.example/search?q=test") == "/search"


def test_get_path_public_export():
    assert public_get_path is get_path


def test_rejects_incomplete_url():
    with pytest.raises(EasyUrlError):
        get_domain("school.example")
    with pytest.raises(EasyUrlError):
        get_path("school.example")
    with pytest.raises(EasyUrlError):
        add_query_param("https://school.example", "", "2")


def test_remove_query_param():
    start = "https://school.example/clubs?page=2&sort=name"
    assert remove_query_param(start, "page") == "https://school.example/clubs?sort=name"
    assert remove_query_param(start, "sort") == "https://school.example/clubs?page=2"
    assert (
        remove_query_param("https://school.example/clubs?page=2", "page")
        == "https://school.example/clubs"
    )
    assert remove_query_param(start, "missing") == start


def test_remove_query_param_keeps_repeated_keys():
    start = "https://school.example/clubs?tag=python&page=2&tag=beginner"
    assert (
        remove_query_param(start, "page")
        == "https://school.example/clubs?tag=python&tag=beginner"
    )


def test_remove_query_param_missing_key_leaves_encoded_url_untouched():
    start = "https://school.example/search?q=art%20club"
    assert remove_query_param(start, "missing") == start


def test_remove_query_param_rejects_bad_key_and_url():
    with pytest.raises(EasyUrlError):
        remove_query_param("https://school.example/clubs?page=2", "")
    with pytest.raises(EasyUrlError):
        remove_query_param("https://school.example/clubs?page=2", 2)
    with pytest.raises(EasyUrlError):
        remove_query_param("school.example/clubs", "page")


def test_remove_query_param_public_imports():
    from py_simple import remove_query_param as public_remove
    from py_simple.easy_url import remove_query_param as module_remove

    assert public_remove is module_remove
    assert (
        public_remove("https://school.example/clubs?page=2", "page")
        == "https://school.example/clubs"
    )
