# CazaLotes

A personal tool for finding vintage furniture and art to put in my own flat in Madrid.

I collect mid-century furniture and Venezuelan naive art, and I was losing hours every week
opening the same auction catalogues one by one. This reads them for me and tells me which
lots are worth a look.

It is not a marketplace, a price comparison site, or a reselling tool. One user, me.

## What it does

**Reads catalogues.** Five Madrid auction houses (Durán, Sala Retiro, Segre, Ansorena,
Alcalá) plus two Shopify shops. Around 2,300 live lots at the moment.

**Scores them against my taste**, which lives in `perfil.py`: Shaker, Barragán, Donald Judd,
Vienna Secession, Danish teak, Venezuelan naive painters, sculpture and busts. And what I
don't want, which matters just as much: religious imagery, gilt carving, Louis XVI
reproductions.

**Reads the catalogue against me.** Spanish auction houses have a precise vocabulary that
most buyers miss. "Atribuido a" means the experts disagree. "Círculo de" means it is not by
the artist at all. "Firmado en plancha" means the signature is printed, not signed. The tool
flags those phrases, because they are where people overpay.

**Works out what it actually costs.** The hammer price is not the price. Each house has its
own buyer's premium (Segre 21.8%, Durán and Sala Retiro 23%, Alcalá 24.2%, Ansorena 25%
below €1,000), and some charge €6 a day in storage if you are slow to collect. The tool adds
all of it up before showing me anything.

**Takes a brief with hard limits.** `encargo.py` holds requests like "a chest of drawers no
wider than 220 cm, under €600, and it has to fit through a 200 cm door". Measurements are not
a preference, they are a constraint. A piece that does not fit is not an opportunity.

## What it deliberately does not do

**It does not bid.** Spanish auction conditions sell everything *cuerpo cierto*, as-is,
explicitly including errors of description, and you have 14 or 15 days to complain. The last
step is a human looking at the thing.

**It does not value anything.** Published research on vision models putting a name to a
painting reports accuracy between 6.7% and 12.6%. A tool that reads labels and stamps is
useful. One that tells you who painted something is lying to you.

**It does not scrape anything that asked not to be scraped.** The five auction houses publish
`robots.txt` files that allow everything. Wallapop forbids `/search` and any URL with a query
string, so there is no adapter for Wallapop and there will not be one. Etsy and Mercado Libre
have official APIs, which is why I am applying for keys instead of working around them.

Everything runs without logging in. One request every three seconds, one pass a day, an
identifiable User-Agent with a real contact address, a full stop on any 403, and no
downloading of lot photographs: it stores the URL and links out.

## Running it

```bash
python3 -m venv .venv
.venv/bin/pip install beautifulsoup4 lxml requests
cp config.py config_local.py    # put your own contact address in it

.venv/bin/python run.py              # read all the houses, then rank
.venv/bin/python run.py --informe    # re-rank what is already stored
.venv/bin/python encargo.py          # run a brief with hard measurements
.venv/bin/python marketplaces.py     # build manual search links for sites with no API
```

## Layout

| File | Job |
|---|---|
| `perfil.py` | My taste, as weights. The only file worth editing often |
| `casas.py` | Each house, its premium, its storage charges, total cost |
| `scraper.py` | Reads the five houses. Rate limiting and stop conditions live here |
| `duran.py` | Durán loads lots over AJAX and needs its own adapter |
| `shopify.py` | Shops with an open `products.json` |
| `puntuar.py` | Scoring, and the catalogue-vocabulary flags |
| `encargo.py` | Briefs with hard dimensional limits |
| `comparables.py` | Past prices. Works, but the matching needs rebuilding |
| `marketplaces.py` | Search links for sites that cannot be read automatically |

## Where it is weak

`comparables.py` matches on shared words, and Alcalá's archive is mostly 18th century Spanish
antiques, so a 1960s sideboard gets compared against a Carlos III writing desk and the verdict
is meaningless. It needs to match within category and period. Until then, do not trust the
number it prints.

The taste profile is my reading of my own taste, which is not the same as my taste. It gets
better when I feed it things I actually chose.

## One finding worth writing down

From Alcalá's own archive, 9,590 pairs of starting price and hammer price:

- **52%** of lots do not sell at all.
- Of those that do, **60%** go at the starting price or below.
- Median ratio of hammer to opening bid: **1.00x**. Only 9% double it.

So roughly three lots in ten are knocked down at the opening bid with nobody bidding against
you. Bidding wars are the exception. Leaving a modest bid on thirty lots beats fighting over
one.
