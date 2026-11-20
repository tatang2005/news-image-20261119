[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/tatang2005/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/tatang2005/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Day — Thursday 19 November 2026

Entry for the make.fun competition **news-image-20261119**: one image that
sums up the world's news of Thursday 19 November 2026.

Bounty page: https://make.fun/bounty/news-image-20261119

The image is a newspaper front page: a dated masthead, six story panels
(the Shenzhen trilateral summit, Ukraine's third strike on the Crimean
Bridge, the Gaza raid amid the ceasefire, COP31 dropping fossil-fuel
language, Anthropic's record IPO, and the ICJ's Myanmar genocide ruling),
and a footer strip with three more of the day's stories (the Greenland
Arctic deal, Bangladesh's deadly lockdown violence, and North Korea's
expanding enrichment at Yongbyon).

## How it works

- `draw.py` draws the front page with PIL (flat geometric icons, big serif
  headlines) and saves it as `entry.png` (1024x1024).
- `main.py` is the entry program: it copies `entry.png` to the output
  directory (`$MAKEFUN_OUTPUT_DIR`, or `/output`).

## Run

```sh
python3 main.py
```

## License

MIT — see `LICENSE`.
