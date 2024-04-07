# Ringram generation

## Install environment

```bash
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

## Generate a puzzle

### 4x4

[4-letter wordlist](./words_4-letters.txt) from <https://copylists.com/words/list-of-4-letter-words/>.

```bash
python ./puzzlegen.py -n 4
```

### 3x3

[3-letter wordlist](./words_3-letters.txt) from <https://copylists.com/words/list-of-3-letter-words/>.

```bash
python ./puzzlegen.py -n 3
```

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

## Run tests

```bash
pytest
```
