# Stardrifter

**WARNING** Not playable yet. I'm currently throwing ideas in a bucket, and see
how they can work out. Please bear with me. It might be a long process.

It's the first time I'm doing this kind of work. **Any** remark, bug report,
note, advice is welcome. Please, please, please help me make this game better.

---

Stardrifter is a tabletop solo role-playing game about being a Trader / Smuggler
in a science-fiction galaxy-wide settings.

In this game you'll be given a spaceship, a few credits, basic weapons and
you'll be free to sail this ship from planets to planets to sell, buy, or even
hijack other stardrifters.

It borrows a lot from
[Pocket Dungeon][Pocket Dungeon], by
Jonathan Gilmour, since the star systems in the galaxy are usually not
pre-generated, but they're made up **during the game itself**, using a few
dice rolls.

Each game would thus be totally different from each other.

---

## Building the website

For those interested into building the HTML documents out of the markdown source,
you'll have to use the `drift.py` tool.

It is *recommended* to use [Virtualenv][venv] beforehand.

```shell
pip install -r requirements.txt
python drift.py build  # to build the docs
python drift.py clean  # to clean the build directory
```

## License

This game is published under the terms of the [CC-BY-SA License][CC-BY-SA License].

[Pocket Dungeon]: http://boardgamegeek.com/boardgame/42361/pocket-dungeon
[CC-BY-SA License]: http://creativecommons.org/licenses/by-sa/3.0/
[venv]: http://pypi.python.org/pypi/virtualenv
