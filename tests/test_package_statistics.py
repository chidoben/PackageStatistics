"""
Unit tests for the Package Statistics module
This file contains unit tests for the Package Statistics module
"""
import pytest
from requests.exceptions import HTTPError

from src.package_statistics import (
    download_file_associated_with_the_architecture,
    parse_file_content_and_print_top_ten_packages,
    pd,
)


def test_download_file_associated_with_the_arch_raises_exception():
    """
    Test that the download_file_associated_with_the_architecture method
    raises an exception when an architecture that doesn't exist is passed as
    input to it.
    """
    invalid_architecture = "unknown_linux_architecture"
    with pytest.raises(HTTPError):
        download_file_associated_with_the_architecture(invalid_architecture)


def test_download_file_associated_with_the_arch_returns_binary_content():
    """
    Test that the file contents returned by the
    download_file_associated_with_the_architecture method is in binary format
    """
    architecture = "arm64"
    file_contents = download_file_associated_with_the_architecture(
        architecture
    )
    assert isinstance(file_contents, bytes)


def test_print_top_ten_packages_correctly_prints_the_top_ten_packages(
    monkeypatch, capfd
):
    """
    Test that the parse_file_and_print_top_ten_packages method
    correctly prints the top ten packages
    """
    fake_file_contents = b"fake_byte_data"
    mock_dataframe = pd.DataFrame(
        {
            "package names": [
                "package 1,package 2,package 3",
                "package 1,package 3",
                "package 4,package 1",
            ]
        }
    )

    def return_mocked_dataframe(*args, **kwargs):
        """
        used by monkeypatch to return a mocked dataframe instead of calling
        the actual pd.read_csv() method.
        """
        return mock_dataframe

    monkeypatch.setattr(pd, "read_csv", return_mocked_dataframe)

    parse_file_content_and_print_top_ten_packages(fake_file_contents)

    # Assert that the correct package is printed as having the most files
    # associated with it
    out, err = capfd.readouterr()
    assert "package 1        3" in out
