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
  - make a base 64 encoder so you can share custom puzzles
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

### Other sizes

Any size is reasonably possible. Larger ones will start to have LOTS of dots/dashes, so these should be very wrappable by this stage.

## Notes on puzzle difficulty

What makes puzzles easier or harder? I'm not sure. Here are some which could, or they might not.

- Double letters (if two opposite letters are the same letter)
- Middle-filled in letter. If a letter is filled in, in the middle, it makes its opposite side twin easier to guess
- Rare letters?
- If there is a row/column with no/few dots (and few dashes), or no/few dashes (and few dots)
- If there is a combination of starting letters which, grammatically, can not result in many words which would fit there

## Notes on swappability

Some words are idempotent under "count the dots/dashes of each letter".

For example, `FAD == FAR` as `D = -..` and `R=.-.`, so ignoring the per-letter order of dots/dashes results in the same count.

These letters can be swapped:

```text
ONE DOT
E

ONE DASH
T

TWO DOTS
I

TWO DASHES
M

THREE DOTS
S

THREE DASHES
O

ONE DOT ONE DASH
A N

TWO DOTS ONE DASH
D R U

ONE DOT TWO DASHES
G K W

TWO DOTS TWO DASHES
C P X Z

THREE DOTS ONE DASH
B L V F

ONE DOT THREE DASHES
J Q Y

FOUR DOTS
H
```
