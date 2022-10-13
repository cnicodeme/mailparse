#!/usr/bin/bash

# It needs python3 -m pip install --user --upgrade setuptools wheel twine

if [ $# -eq 0 ]
  then
    echo "Please provide a valid tag, like x.x.x"
fi

# First, we push to Git with the new tag version
git add --all
git commit -a
git push origin master
git tag $1
git push orign $1

python3 -m build
python3 -m twine upload dist/*