# news-image-18-frontpage-v2

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/sussybakka0110new/news-image-18-frontpage-v2/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/sussybakka0110new/news-image-18-frontpage-v2/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A dense, legible front page for Wednesday 18 November 2026: 45 short verified
headlines in three themed columns, a very large date banner, a simplified world
map with ten flashpoint markers, and a sourced footer.

`render.py` draws the whole 1024x1024 PNG with the Python standard library only
(`struct` and `zlib`, plus a hand-coded 5x7 bitmap font). The committed
`entry.png` is copied to the grader's output by `main.py`.

## Run it

```sh
python3 render.py            # regenerate the committed entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The image is an 8-bit RGB PNG, 1024 by 1024 pixels and about 25 KiB, well
inside the one-megabyte limit. Both runs of `main.py` write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
