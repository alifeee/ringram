# Ringram puzzles

![Image of ringram puzzle, showing a grid of characters, surrounded in dots and dashes](images/ringram.png)

## Development

### Install

```bash
npm install
```

### Develop

```bash
npm run dev
```

### Build

The site files get built into `./_site/`.

```bash
npm run build
```

## Nice features

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
  - make style a bit cooler
  - add footer with references
  - check on different device sizes
  - check on different browsers
- add new puzzle every day with CRON CI
