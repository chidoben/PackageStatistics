"""
Package Statistics module
This module contains an implementation of a console application that
prints the top 10 packages with the most files associated with them
"""
import io
import logging

import click
import pandas as pd
import requests
from requests.exceptions import HTTPError

POSSIBLE_ARCHITECTURES = [
    "amd64",
    "arm64",
    "armel",
    "armhf",
    "i386",
    "mips64el",
    "mipsel",
    "ppc64el",
    "s390x",
    "source",
    "all",
]


def download_file_associated_with_the_architecture(architecture: str) -> bytes:
    """
    Downloads the file associated with the user selected architecture from a
    Debian mirror.
    :param architecture: The architecture associated with the file to be
                          downloaded
    :type architecture: string
    :return: The file contents in bytes.
    :rtype: bytes
    """
    url = f"http://ftp.uk.debian.org/debian/dists/stable/main/Contents-{architecture}.gz"  # noqa: E501
    try:
        response = requests.get(url)

        # Raise an exception if the get request wasn't successful
        response.raise_for_status()
    except HTTPError as e:
        logging.exception("HTTP error occurred")
        raise e
    except Exception as e:
        logging.exception("Other error occurred")
        raise e

    # Return the file contents in bytes as returned by the response object
    return response.content


def parse_file_content_and_print_top_ten_packages(file_contents: bytes):
    """
    Parses the file contents and prints the top ten packages that have the
    most files associated with them.
    :param file_contents: Contents of the downloaded file in bytes.
    :type file_contents: bytes.
    """
    # Read the file contents into a pandas dataframe.
    # Here we are assuming that the file name and package names are
    # separated by one or more spaces. While the package names are separated by
    # commas. As advised in the documentation,
    # https://wiki.debian.org/DebianRepository/Format?action=show&redirect=RepositoryFormat#A.22Contents.22_indices
    # we will be ignoring any lines not conforming to this scheme using
    # on_bad_lines = "skip".
    df = pd.read_csv(
        io.BytesIO(file_contents),
        delim_whitespace=True,
        compression="gzip",
        index_col=False,
        on_bad_lines="skip",
        low_memory=False,
        header=None,
        usecols=[1],
    )

    # For each row with comma separated package names, split the package names
    # by commas and put each package name in its own distinct row. After this
    # step, each package name will be in its own row.
    # This way we can correctly count the lines where we have
    # multiple packages separated by commas that are associated with one file
    df = df.apply(lambda x: x.str.split(",").explode()).reset_index(drop=True)

    # Count the number of times each package appears in the dataframe.
    # This will give us the packages with the most files associated with them.
    # We then select the top 10 packages and print their qualified package
    # names and the number of files associated with them
    print(
        "----------Qualified package name------------- | ---Number of "
        "files---"
    )
    print(df.value_counts().head(10))


@click.command()
@click.option(
    "--architecture",
    prompt="Please enter the architecture "
    "associated with the compressed "
    "contents"
    " file you wish to download",
    help="Architecture (amd64, arm64, mips etc.)",
    type=click.Choice(POSSIBLE_ARCHITECTURES, case_sensitive=False),
)
def run_application(architecture: str):
    """
    Console application that prints the top 10 packages with the most files
    associated with them.\n
    When you run the application, you will be prompted to enter the
    architecture associated with the file you wish to download. Alternatively,
    you can also provide the architecture using the --architecture option.

    """
    file_contents = download_file_associated_with_the_architecture(
        str(architecture).lower()
    )
    parse_file_content_and_print_top_ten_packages(file_contents)


if __name__ == "__main__":
    run_application()
