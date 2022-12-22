#!/bin/bash
deleteDir() {
    if [ -d $1 ]; then rm -rf $1; fi
}
deleteFile() {
    if [ -f $1 ]; then rm -f $1; fi
}
echo "Cleaning ..."
deleteDir .pytest_cache
deleteDir .mypy_cache
deleteDir allure-results
deleteDir allure-report
deleteDir htmlcov
deleteDir build
deleteDir dist
deleteDir bounciepy.egg-info
deleteFile .coverage
deleteFile coverage.xml

echo "Linting ..." &&
    pylint bounciepy/ tests/ &&
    echo "Type checking ..." &&
    mypy bounciepy/ &&
    echo "Testing ..." &&
    pytest &&
    echo "Reporting ..." &&
    allure generate --clean
if [[ ! -n $1 ]]; then
    echo "Building the distribution ..." &&
        python setup.py sdist bdist_wheel
else
    echo "Distribution build skipped."
fi
echo "Done."
