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

.venv/bin/python run.py              # read the live catalogues, then rank
.venv/bin/python shopify.py          # read the two Shopify shops
.venv/bin/python etsy.py             # Etsy, through its official API (needs keys, see below)
.venv/bin/python vista.py            # build the page: datos/vista.html
open datos/vista.html                # browse, search, vote

.venv/bin/python run.py --informe    # re-rank what is already stored, in the terminal
.venv/bin/python run.py --historico  # also pull the past-sales archive (hours, do it once)
.venv/bin/python marketplaces.py     # build manual search links for sites with no API
```

## Etsy

Etsy is read through its official Open API v3, under a personal-access app approved on
2 October 2026. It needs two values in `config_local.py`, which is never committed:
`ETSY_KEYSTRING` and `ETSY_SHARED_SECRET`. Etsy requires both, joined by a colon, in the
`x-api-key` header.

Two of Etsy's API terms shape how this works. Content may not be shown more than 24 hours
older than on Etsy itself, and may not be stored longer than needed. So Etsy listings go to
`datos/etsy.json`, which is overwritten on every run and never accumulated, and the page
drops them automatically once they are more than 24 hours old. The page also carries the
trademark notice the terms require.

Each Etsy listing shows the original price and currency; the euro figure used for filtering
is an approximate conversion. Listings Etsy marks as recent are flagged as new rather than
vintage, and shops outside the EU are flagged for customs and import VAT.

Etsy sellers pad titles and the materials field with lists of designer names for search
("eames, rietveld, cadovius, le corbusier"). Titles are cut back to the part that describes
the piece, padded materials are dropped, and a listing that names four or more designers only
scores for the top two and is flagged. English catalogue vocabulary ("in the style of",
"replica", "attributed to") is flagged the way "estilo" and "atribuido a" are, ignoring the
harmless uses ("we never sell reproductions", "reproduction cloth cord"). Etsy's own size
fields are usually empty, so measurements are also read from labelled text in the
description ("height 81.5 cm, width 55 cm").

## The page

`vista.py` writes one self-contained HTML file. Everything on sale that does not clash
outright with my taste goes in, about 4,000 lots, drawn 120 at a time.

The search panel takes a brief the way I would say it out loud: what kind of thing
(the page expands "storage" into cómoda, cajonera, aparador, credenza and the rest of the
catalogue vocabulary), colour, width, height and depth separately, whether it has to fit
through a door, a ceiling on the real cost with the premium included, materials, period,
and words to exclude. Briefs can be saved by name.

Under the panel, the same search is offered as ready-made links to Catawiki, Wallapop,
Milanuncios, eBay, Etsy, Vinted and Todocolección, with the query and the price ceiling
already filled in. Those sites cannot be read automatically, but they can be opened in one
click. Catawiki sits behind Akamai and returns 403 to any automated request, `robots.txt`
included, so it stays manual; its own "Guardar búsqueda" sends alerts. Its buyer fee is 9%
plus a fixed 3 €, VAT included (buyer terms, September 2026).

Each lot shows four separate scores (taste, opportunity, logistics, confidence) rather than
one opaque number, why it matched, and what the catalogue wording gives away. Votes are kept
in the browser and exported as JSON, which is how the taste profile gets corrected.

Photographs come at 500 px in the grid and at full size in the detail view. The listing
pages only link a 260 px thumbnail, which is why an earlier version looked blurry.

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
| `comparables.py` | Past hammer prices, matched within category and period |
| `vista.py` | Builds the page: scores, attributes, image sizes |
| `plantilla.py` | The page itself: search panel, grid, detail view |
| `marketplaces.py` | Search links for sites that cannot be read automatically |

## Where it is weak

`comparables.py` now only compares within the same category and a compatible period, uses
hammer prices where the archive has them, and refuses to give a verdict on fewer than six
comparables. That fixed the nonsense (it used to compare a 1960s sideboard against a
Carlos III writing desk), but it exposed the real limit: Alcalá's archive has 465 furniture
lots and nearly all are antiques. It gives a verdict on about a quarter of the lots that
match my taste, mostly sculpture, painting and ceramics. For mid-century furniture there is
no base to compare against yet.

The storage I am actually looking for is rare in these seven sources: nine lots out of
4,334 at last count. For that kind of piece the private-sale sites are where the stock is,
and those are the ones that cannot be read.

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
