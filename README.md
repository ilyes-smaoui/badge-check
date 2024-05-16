# badge-handler
## Introduction
Small program to check a PNG file against avatar requirements (badge shape, image size, etc.)

## Quick description
The program goes through three consecutive steps :
- first it checks the image size : it has to be 512x512
- then it checks the badge shape : it has to be round
- then it analyzes the colors in the image and computes to verify that they convey a happy feeling, using a hard-coded default "happy profile" (might be improved in later versions to be easily personalizable)

## Command-line usage
```./badge_check.py [filename] [score]```

`filename` : filename for the png badge file

`score` : minimum (color) score to satisfy (between 0 and 1)
