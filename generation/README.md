# Ringram generation

## Install environment

```bash
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

## Generate a puzzle

To-Do

## Generate the YAML representation of a puzzle

An example command is

```bash
python puzzleyaml.py -w BIRD BORN DOVE NOSE -r 1 12
```

Which would generate the YAML representation of the puzzle:

```text
B - - -
-     -
-     -
- - - E
```

For more information see the docstring in [`puzzleyaml.py`](./puzzleyaml.py).
