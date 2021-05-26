### To Install
    pip install -U pytest
    -U flag to upgrade/install newest version of pytest

### To Run
    python3 -m pytest
    -m flag to run as a module (needed)
    
    python3 -m pytest -q (filename)
    -q/quiet will keep the output short

    example: python3 -m pytest -q test_main.py

    python3 -m pytest -k (expression)
    -k will only run tests wich match the substring expression

    example: python3 -m pytest TestClass (will only run tests within the TestClass)

    
### Documentation
[Pytest.org](https://docs.pytest.org/en/6.2.x/contents.html#)