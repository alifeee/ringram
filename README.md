# Ringram puzzles

See [`./website/`](./website/) and [`./generation/`](./generation/)

![Image of ringram puzzle, showing a grid of characters, surrounded in dots and dashes](images/ringram.png)

## Nice features

- UI
  - "show solution" button
  - "check solution" button
  - "clear" button
  - there is no "red" dot/dash if the row/column has 0 to begin with
  - press up/down arrow keys to move box (if cursor is in reasonable place)
      logic: if a key is pressed (up), collect a list of inputs which are reasonable and (e.g., with a function which turns flat inputs into a list of "0, 3, and 6 are above you!". Then, filter for "disabled", and if there's one left...) focus it!
  - pressing backspace/left/right skips over disabled inputs
  - toggle/inputs on cheat sheet for:
    - hide/show vowels
    - hide/show letters with "exactly N dots & M dashes"
- hashing & generating
  - think of puzzle hash (number of dots/dashes plus starting letters)
  - think of solution hash (just the 12 letters)
  - make a validator to check solution hash against puzzle hash
  - make puzzle generator
- difficulty
  - make "easy" puzzle (with N letters revealed)
  - make "medium" puzzle (with M letters revealed)
  - make "hard" puzzle (with O letters revealed)
- usability features
  - save state (entered letters) in local storage (but only for specific puzzle hash)
- style
  - wrap dots when more than X
  - make style a bit cooler
  - add footer with references
  - check on different device sizes
  - check on different browsers
- add new puzzle every day with CRON CI
