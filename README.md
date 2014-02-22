# Yeahtzee - Battle of the Yahtzee bots

## Rationale

> Stef: "When playing Yahtzee, it's always best to leave the Yahtzee option open."
> 
> Bart: "Then why are you always losing?"

**Yeahtzee** is a battleground to discover the best strategy in [Yahtzee](http://en.wikipedia.org/wiki/Yahtzee). It faces off different Yahtzee engines over a number games, collecting statistics along the way.

## Combatants / Engines

* [automahtzee](engines/automahtzee.py) by [@cfilorvy](https://github.com/cfilorvy)
* [jayzee](engines/jayzee.py) by [@megasnort](https://github.com/megasnort)

## How to commence the battle

```shell
python common/gerard.py -t 1 -g 2 -e automahtzee jayzee
```

### Options

```shell
-t  number of threads
-g  number of games
-e  engines to participate in the battle
```
