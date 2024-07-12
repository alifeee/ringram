# Ringram puzzles

<https://ringram.alifeee.co.uk/>

See [`./website/`](./website/) and [`./generation/`](./generation/)

![Image of ringram puzzle, showing a grid of characters, surrounded in dots and dashes](images/ringram.png)

## Nice features

- UI
  - "show solution" button - currently each page does not *know* the solution - could either
    - send solution to page (hidden?)
    - request the solution from the server
    - send the word list and algorithmically solve the puzzle in JS (this is worth writing anyway to check if puzzles have a unique solution, or more than one)
  - "check solution" button - this can either do:
    - simple: check if the expected dots/dashes match used dots/dashes (might get nonsense/wrong solution)
    - complex: checek against solution (see above for how to get solution)
  - "clear" button
  - press up/down arrow keys to move box (if cursor is in reasonable place)
      logic: if a key is pressed (up), collect a list of inputs which are reasonable and (e.g., with a function which turns flat inputs into a list of "0, 3, and 6 are above you!". Then, filter for "disabled", and if there's one left...) focus it!
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
  - add statistics
- style
  - wrap dots when more than X
  - make style a bit cooler
  - add how to play guide
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

## Installation on a server

### Copy code

```bash
mkdir -p /var/www/
git clone git@github.com:alifeee/ringram.git /var/www/ringram
cp /var/www/ringram/website/_data/puzzles.yaml.example /var/www/ringram/website/_data/puzzles.yaml
```

### Generate puzzles

See [generation](./generation) for more

```bash
cd /var/www/ringran/generation
python puzzlegen.py -n 3
python puzzlegen.py -n 4
python puzzlerank -i puzzles_3x3.txt -o unique > puzzles_3x3_sorted.txt
python puzzlerank -i puzzles_4x4.txt -o unique > puzzles_4x4_sorted.txt
```

### Get Telegram API token

- message @BotFather to create a bot
- POST to `https://api.telegram.org/bot<api_token>/getMe` to check API token
- message bot, then to find the chat id POST to `https://api.telegram.org/bot<api_token>/getUpdates`
- send a message: POST to `https://api.telegram.org/bot<api_token>/sendMessage?chat_id=<chat_id>&text=hello+world`

```bash
cd /var/www/ringram
cp .env.example .env
nano .env
```

### Install modules for website

```bash
cd /var/www/ringran/website
npm install
npm run build
```

### Install crontab

There are two: one to generate new words, which runs 12 hours before the one which updates the website (so words can be changed)

```bash
crontab -e
```

then put in these cron tasks:

```cron
0 12 * * * /var/www/ringram/next.sh >> /var/www/ringram/cron.log 2>&1
0 0 * * * /var/www/ringram/update.sh >> /var/www/ringram/cron.log 2>&1
```
