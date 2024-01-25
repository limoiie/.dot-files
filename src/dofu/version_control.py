import shlex
import typing as t

from dofu import shutils


def normalize_repo_url(url: str):
    """
    Normalize a git repo url to a standard format of:
        https://<domain>/<user>/<repo>
    """
    # Remove leading and trailing whitespace and slashes
    url = url.strip(" /\n\r")

    # Remove .git extension, if present
    if url.endswith(".git"):
        url = url[:-4]

    # Check if the URL is in SSH format
    # noinspection HttpUrlsUsage
    if url.startswith("git@"):
        # Replace colon separator with forward slash
        url = url.replace(":", "/")
        # Replace git@ with https://
        url = url.replace("git@", "https://")

    # Check if the URL is in HTTP format
    elif url.startswith("http://"):
        # Replace http:// with https://
        # noinspection HttpUrlsUsage
        url = url.replace("http://", "https://")

    return url


def log(
    *opts: str, repo_path: str, path: str, revision: str, encoding: str = None
) -> t.Union[str, bytes]:
    """
    Get the log of a rel path.

    If no path is given, the project root is used.
    If no revision is given, the default HEAD revision is used.

    :param opts: options to pass to git log.
    :param repo_path: where the repo has been cloned to
    :param path: a rel path related to the project root.
    :param encoding: the encoding of the output.
    :param revision: the revision to check.
    :return: the log of the path.
    """
    return shutils.check_output_no_side_effect(
        f"git log {shc(opts)} {revision} -- {path}",
        encoding=encoding,
        cwd=repo_path,
    )


def clone(*opts: str, repo: str, repo_path: str = "", cwd: str = None) -> None:
    """
    Clone a repo to a path.

    :param opts: options to pass to git clone
    :param repo: url to the repo
    :param repo_path: where the repo should be cloned to
    :param cwd: current working directory
    """
    shutils.check_call(f"git clone {shc(opts)} {repo} {repo_path}", cwd=cwd)


def pull(*opts: str, repo_path: str) -> None:
    """
    Pull a repo cloned at a local path.

    :param opts: options to pass to git pull
    :param repo_path: where the repo having been cloned to
    """
    shutils.check_call(f"git pull {shc(opts)}", cwd=repo_path)


def fetch(*opts: str, repo_path: str) -> None:
    """
    Fetch a repo cloned at a local path.

    :param opts: options to pass to git fetch
    :param repo_path: where the repo having been cloned to
    """
    shutils.check_call(f"git fetch {shc(opts)}", cwd=repo_path)


def checkout(*opts: str, repo_path: str, revision: str) -> None:
    """
    Checkout a path at a revision.

    :param opts: options to pass to git checkout
    :param repo_path: where the repo having been cloned to
    :param revision: the revision to check.
    """
    shutils.check_call(f"git checkout {shc(opts)} {revision}", cwd=repo_path)


def remote(*opts: str, repo_path: str) -> None:
    """
    Remote related operations.

    :param opts: options to pass to git remote
    :param repo_path: where the repo having been cloned to
    """
    shutils.check_call(f"git remote {shc(opts)}", cwd=repo_path)


def remote_get_url(*opts: str, repo_path: str, name: str = "origin") -> None:
    """
    Get the url of a remote.

    :param opts: options to pass to git remote get-url
    :param repo_path: where the repo having been cloned to
    :param name: the name of the remote.
    """
    return normalize_repo_url(
        shutils.check_output_no_side_effect(
            f"git remote get-url {shc(opts)} {name}", cwd=repo_path, encoding="utf-8"
        )
    )


def checkout_paths(*opts: str, repo_path: str, paths: t.List[str]) -> None:
    """
    Checkout a path at a revision.

    :param opts: options to pass to git clone
    :param repo_path: where the repo having been cloned to
    :param paths: a list of paths to check out.
    """
    shutils.check_call(f"git checkout {shc(opts)} -- {shc(paths)}", cwd=repo_path)


def default_branch(repo_path: str) -> str:
    return shutils.check_output_no_side_effect(
        "git symbolic-ref refs/remotes/origin/HEAD --short",
        encoding="utf-8",
        cwd=repo_path,
    ).strip()[len("origin/") :]


def add_one(*opts: str, repo_path: str, path: str) -> None:
    """
    Add one path to git.

    :param opts: options to pass to git clone
    :param repo_path: where the repo having been cloned to
    :param path: the path to add.
    """
    shutils.check_call(f"git add {shc(opts)} {path}", cwd=repo_path)


def add(*opts: str, repo_path: str, paths: t.List[str]) -> None:
    """
    Add a path to git.

    :param opts: options to pass to git clone
    :param repo_path: where the repo having been cloned to
    :param paths: a list of paths to add.
    """
    shutils.check_call(f"git add {shc(opts)} {shc(paths)}", cwd=repo_path)


def current_commit_id(repo_path) -> str:
    """
    Get the current commit id of a repo.

    :param repo_path: where the repo having been cloned to
    :return:
    """
    return last_commit_id_of(repo_path=repo_path)


def last_commit_id_of(*, repo_path, revision: str = "", path: str = "") -> str:
    """
    Get the last commit id of a rel path.

    :param path: a rel path related to the project root.
    :param repo_path: where the repo having been cloned to
    :param revision: the revision to check.
    :return: the last commit id of the path.
    """
    return log(
        "-1",  # only one commit
        "--pretty=%H",  # only the commit id
        repo_path=repo_path,
        path=path,
        revision=revision,
        encoding="utf-8",
    ).strip()


def shc(opts) -> str:
    """
    Convert a list of options to a string that can be used in shell.

    :param opts: A list of options.
    :return: A string that can be used in shell.
    """
    return shlex.join(opts)
