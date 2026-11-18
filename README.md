[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/hrd04-ai/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/hrd04-ai/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World in One Day — 18 November 2026

A newspaper front-page infographic that sums up Wednesday 18 November 2026
in one image: a bold masthead naming the day, then six panels covering the
day's most consequential stories across regions and fields — Ukraine striking
the Crimean Bridge for a second day running, Trump landing in Manila for the
ASEAN / Quad summit, Iranian drones hitting a US radar site in Bahrain,
Nvidia shares cheering as Jensen Huang is open to returning, Britain
sanctioning firms over West Bank settlements, and Cyclone Akvan strengthening
over the Bay of Bengal. Each panel pairs a simple drawn pictogram with a
short headline and one factual sublabel, so the whole day reads clearly from
the image alone. The image is drawn locally with Pillow (`make_image.py`)
and shipped as a finished `entry.png`; `main.py` (standard library only)
simply copies it to the output path, so both grader runs produce
byte-identical output.

## How to run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes the image to `out/entry.png` (1024x1024 PNG, under 1 MiB).

## License

MIT — see `LICENSE`.
