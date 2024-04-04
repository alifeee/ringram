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
    - sort letters by number of dots/number of dashes/alphabetically
- hashing & generating
  - think of puzzle hash (type (4x4, 3x3), number of dots/dashes plus starting letters)
  - think of solution hash (just the 12 letters)
  - make a validator to check solution hash against puzzle hash
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

## 3x3

What is 4x4 specific? Some things. To make 3x3 (or other sizes) possible...

Some things could be changed to be "last of type" or "first of type" instead of hard-indexed `0..4`.

Some others will have to be switched based on the puzzle size (such as functions which transform the flat list of inputs into a puzzle). Maybe I'll have to template language the CSS file...

### Other sizes

Any size is reasonably possible. Larger ones will start to have LOTS of dots/dashes, so these should be very wrappable by this stage.

## Notes on puzzle difficulty

What makes puzzles easier or harder? I'm not sure. Here are some which could, or they might not.

- Double letters (if two opposite letters are the same letter)
- Middle-filled in letter. If a letter is filled in, in the middle, it makes its opposite side twin easier to guess
- Rare letters?
- If there is a row/column with no/few dots (and few dashes), or no/few dashes (and few dots)
- If there is a combination of starting letters which, grammatically, can not result in many words which would fit there
