# Hephaestus

## Table of Contents
1. [Objective](#objective)
2. [Use](#use)
    - [Installation](#installation)
    - [Testing](#testing)
    - [Generating Documentation](#generating-documentation)
3. [Inspirations](#inspirations)
4. [Future Plans](#future-plans)
    - [Short Term Goals](#short-term-goals)
    - [Long Term Goals](#long-term-goals)


## Objective

The objective of this project was/is to stop repeating myself. I've gotten tired of rewriting the same modules and utilities
for various professional and hobby project.

Started in December 2024, well... technically, since about 2022.

## Use

Project is free for use and uploaded to [PyPi under the name hephaestus-lib](https://pypi.org/project/hephaestus-lib/).

Unfortunately, someone already took the name Hephaestus on PyPi so...

All modules are still referenced like so:

```
# myfile.py

from hephaestus.common.colors import Colors
from hephaestus.testing.pytest.fixtures import *

```

While not intentionally developed to be cross-platform, most of the stuff in here is. It just didn't cost that that much more effort 
or brainpower to avoid.

This library is not intended to be used as a template or guide, but it can definitely can be used as "inspiration." Please link back to this repo or [MalakaiSpann.com](https://malakaispann.com) if you do.

### Installation

```bash
pip install hephaestus-lib
```

### Testing

```bash
scripts/run_pytest
```

### Generating Documentation
```bash
scripts/generate_documentation
```

Friendly reminder: don't be a weirdo who steals source code. Even when credited, it's still pretty shady to straight copy someone else's work. The occasional peak when you're stuck is fine, but learn how to do it yourself... it'll get you much farther!

## Future Plans

This is likely going to be a Work-In-Progress for quite some time. There's lots to do even with the small amounts of 
code already in here.

I plan on updating/improving this library as long as I use Python 🙂.  

### Short Term Goals
- Get sane CI pipeline together.
    - A lot of the scripts are already there, just kinda need to set everything up to talk to one another.
- Finish documentation. Get it together man.
- Implement code coverage reporting. This is always a good step
- Knock out some unit and functional tests. Many of the things in here are 

### Long Term Goals
- World Peace
- Afford a house
- Live in Japan

Feel free to suggest improvements or get down and dirty (with protection of course... a merge request – I mean a merge request).

Thanks, 

\- Kay