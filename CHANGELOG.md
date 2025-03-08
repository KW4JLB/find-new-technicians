# Unreleased

* Removed shebang interpreters
* Updated README usage
* Added License to repo
* Added Changelog to repo
* Renamed `find-new-technicians.py` to `find-new-license-grants.py` for [issue #2 FIX(rename repo and script to be accurate)](https://github.com/KW4JLB/find-new-technicians/issues/2)
* Updated wording in `README.md` to reflect rebranding for [issue #2 FIX(rename repo and script to be accurate)](https://github.com/KW4JLB/find-new-technicians/issues/2)
* Added Github Pull request Template in `.github/PULL_REQUEST_TEMPLATE.md`
* Added `CODEOWNERS.md`

# v1.1.0
* Added Argument (`-D`, `--download-only`) to Only Download the FCC ULS Database files
* Added Argument (`-d`, `--download`) to download FCC ULS Database and continue filtering results
* Added Argument Checking to make sure `-z`/`--zipcode` and `-m`/`--months` are defined when NOT using `-D`/`--download-only` arguments

# v1.0.2
* Uncommenting out `get_license()` call from previous development

# v1.0.1
* Fixed License status of Terminated to Active
* Fix reading in passed dataframe instead of reading file for filtering out results

# v1.0.0
* Initial Code Release
