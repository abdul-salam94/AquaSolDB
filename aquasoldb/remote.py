# -*- coding: utf-8 -*-
"""Fetch a release from its archive on Zenodo, once, into a cache on disk.

Nothing here runs unless `download()` is called: importing the package never goes
online, and `release_folder()` only looks at a copy already in the cache.  The archive
record is found from the dataset's concept DOI; every file of the record is checked
against the record's own hash list before anything is kept, and the unpacked release is
then checked against its own checksum list.  A file that does not match stops the
download and nothing is written to the cache.

The cache is `cache=` if given, else the `AQUASOLDB_CACHE` environment variable, else
`~/.cache/aquasoldb`; each release sits in its own folder named by its version.
"""
import hashlib
import io
import json
import os
import shutil
import tempfile
import zipfile

#: The DOI that names the database (it resolves to the newest version on Zenodo).
CONCEPT_DOI = "10.5281/zenodo.22870466"
#: The archive's records interface.
ZENODO_API = "https://zenodo.org/api"
#: Set this to keep downloaded releases somewhere other than `~/.cache/aquasoldb`.
AQUASOLDB_CACHE_ENV = "AQUASOLDB_CACHE"
_TIMEOUT_S = 120


def _get(url):
    """The bytes at `url`.  The one place this package goes online."""
    import urllib.request
    request = urllib.request.Request(url, headers={"Accept": "application/json, */*"})
    with urllib.request.urlopen(request, timeout=_TIMEOUT_S) as response:
        return response.read()


def cache_folder(cache=None):
    """The cache folder: `cache`, else `AQUASOLDB_CACHE`, else `~/.cache/aquasoldb`."""
    if cache is None:
        cache = os.environ.get(AQUASOLDB_CACHE_ENV) or os.path.join(
            os.path.expanduser("~"), ".cache", "aquasoldb")
    return os.path.abspath(os.path.expanduser(os.fspath(cache)))


def _release_dir(cache, version):
    return os.path.join(cache_folder(cache), version)


def cached_release(version=None, cache=None):
    """The cached copy of `version` (default: the release this package reads), or None."""
    from . import DATASET_VERSION
    from .tables import _holds_the_data
    path = _release_dir(cache, _label(version if version is not None else DATASET_VERSION))
    return path if _holds_the_data(path) else None


def _label(version):
    version = str(version).strip()
    return version[1:] if version[:1] in ("v", "V") else version


def _record_id(doi):
    prefix = "10.5281/zenodo."
    if not doi.startswith(prefix) or not doi[len(prefix):].isdigit():
        raise ValueError("%r is not a Zenodo DOI" % doi)
    return doi[len(prefix):]


def _json(url):
    return json.loads(_get(url).decode("utf-8"))


def _find_record(version):
    """The archive record whose version is `version`, among the concept DOI's versions."""
    url = "%s/records/%s/versions?size=200" % (ZENODO_API, _record_id(CONCEPT_DOI))
    hits = _json(url).get("hits", {}).get("hits", [])
    found = [h for h in hits if _label((h.get("metadata") or {}).get("version", "")) == version]
    if len(found) != 1:
        listed = sorted({_label((h.get("metadata") or {}).get("version", "")) for h in hits})
        raise LookupError("the archive (concept DOI %s) holds %d records of version %s; "
                          "versions there: %s" % (CONCEPT_DOI, len(found), version,
                                                  ", ".join(listed) or "none"))
    return found[0]


def _checked(record, entry):
    """The bytes of one record file, after its hash matched the record's hash list."""
    key = entry["key"]
    algorithm, _sep, digest = (entry.get("checksum") or "").partition(":")
    if not digest or algorithm not in hashlib.algorithms_guaranteed:
        raise ValueError("the record lists no usable hash for %s (%r); nothing is kept"
                         % (key, entry.get("checksum")))
    url = (entry.get("links") or {}).get("self") or "%s/records/%s/files/%s/content" % (
        ZENODO_API, record["id"], key)
    data = _get(url)
    got = hashlib.new(algorithm, data).hexdigest()
    if got != digest.lower():
        raise ValueError("%s does not match the archive record's %s hash: expected %s, got "
                         "%s. The download is incomplete or the file is not the archived "
                         "one; nothing is kept." % (key, algorithm, digest, got))
    return data


def _safe_extract(archive, target):
    with zipfile.ZipFile(io.BytesIO(archive)) as zf:
        for member in zf.namelist():
            parts = member.replace("\\", "/").split("/")
            if member.startswith(("/", "\\")) or ".." in parts or ":" in parts[0]:
                raise ValueError("the archive names a path outside its folder: %r" % member)
        zf.extractall(target)


def _release_root(folder):
    """`folder` itself, or the one folder at or below it that holds the release."""
    from .tables import _holds_the_data
    for dirpath, _dirs, _names in os.walk(folder):
        if _holds_the_data(dirpath):
            return dirpath
    return None


def download(version=None, cache=None):
    """Fetch release `version` (default: the one this package reads) into the cache and
    return its folder.  A copy already in the cache is checked and returned without going
    online.

    Every file of the archive record is checked against the record's hash list, and the
    release against its own checksum list; any mismatch raises and leaves the cache as it
    was.  Pass the returned folder as `root=`, or let `release_folder()` find it.
    """
    from . import DATASET_VERSION
    from .tables import verify_checksums
    version = _label(version if version is not None else DATASET_VERSION)
    target = _release_dir(cache, version)
    if cached_release(version, cache) is not None:
        verify_checksums(root=target)
        return target
    record = _find_record(version)
    entries = record.get("files") or []
    if not entries:
        raise ValueError("the archive record of version %s lists no files" % version)
    os.makedirs(cache_folder(cache), exist_ok=True)
    staging = tempfile.mkdtemp(prefix=".download-", dir=cache_folder(cache))
    try:
        for entry in entries:
            data = _checked(record, entry)
            if entry["key"].lower().endswith(".zip"):
                _safe_extract(data, staging)
            else:
                path = os.path.join(staging, *entry["key"].split("/"))
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(data)
        root = _release_root(staging)
        if root is None:
            raise ValueError("the archive record of version %s does not unpack to an "
                             "AquaSolDB release" % version)
        verify_checksums(root=root)
        if os.path.exists(target):
            shutil.rmtree(target)
        os.replace(root, target)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return target
