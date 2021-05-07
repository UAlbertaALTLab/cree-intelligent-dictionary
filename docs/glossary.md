analysis
===================
[analysis]: #analysis
[analyses]: #analysis
[linguistic analysis]: #analysis
[linguistic breakdown]: #analysis

_also, **linguistic analysis** or **linguistic breakdown**_.

An **ordered** set of the [lemma][] and [morphosyntactic features][]
that can describe an [inflected wordform][wordform].

It _minimally_ consists of:

 - at least one [lemma][]
 - at least one feature, stating the wordform's [word class][]

### Example

One possible linguistic analysis of the [wordform][] "sabía" in
Spanish is:

    saber+V+Past+1Sg

In other words, the breakdown is:

 - It's a form of _saber_ (the lemma)
 - It's a _verb_
 - It's _past-tense_
 - It's actor is _first-person, singular_

Contains
--------

 - **1 or more** [lemmas][]
 - **1 or more** [morphosyntactic features][]

Describes
---------

 - **1** [wordform][]; note, a single **wordform** can have multiple
   distinct analyses.


conjugation
===========
[conjugation]: #conjugation
[conjugations]: #conjugation

A type of [inflectional category][] for the verb word class.


conjugator
==========

(_informal_) a tool that generates a [paradigm][].

[conjugator]: #conjugator

N.B.: people ask for a conjugator, even when asking to generate noun
wordform!


declension
==========
[declension]: #declension

A type of [inflectional category][] for the noun word class.


definition
==========
[definition]: #definition
[definitions]: #definition

One of possibly several meanings of the [head][].

Part of
-------

-   **1** [dictionary entry][]

Describes
---------

*  **1** [head][]


derivational breakdown
======================
[derivational breakdown]: #derivational-breakdown

A derivational breakdown of a wordform contains different morphemes that makes up the wordform.

Example
--------

-   _atahkw_ + _is_ + _iw_ is the derivational breakdown of _acâhkosiwiw_
-   _star_ + _let_ + _ify_ is the derivational breakdown for the coined English word _startletify_ (to make something a little star)


derivational paradigm
=====================
[derivational paradigm]: #derivational-paradigm

The collection of all possible [derived forms] belonging to a lemma.

### Part of

 - **1** [lemma]

### Contains

 - **1** or more [wordforms]


derived form
============
[derived form]: #derived-form
[derived forms]: #derived-form

A new [wordform] created from a [lemma]; this new wordform has a separate lemma with its own [inflectional paradigm][paradigm]. A derived wordform can belong to a different [word class] than the original source stem.

## Part of

 - **1** [derivational paradigm]

dictionary
==========
[dictionary]: #dictionary

???

dictionary entry
================
[dictionary entry]: #dictionary-entry
[dictionary entries]: #dictionary-entry

The main content of a [dictionary][]. Consists of the [head][] (in one or
more [orthographical representations][]), the [word class][], and the
[definitions][].

Part of
-------

-  **1** [dictionary][]

Contains
--------

-   **1** [head][]
-   **1** or more [definitions][]
-   **1** [word class][], if the [head][] is a [word form][]

See also
-------

-  [source language][]
-  [target language][]


dictionary source
=================
[source]: #source
[dictionary source]: #dictionary-source

An edited repository of [dictionary entries]. A dictionary source has at
least one of the following:

 - an editor/editors
 - an author/authors

A dictionary sources provides at least one or more [dictionary entries].

A dictionary source may have other bibliographic metadata, like a book
or a publication.


indeclinable particle
=====================

(In Plains Cree linguistics) The word class of terms that do not
inflect. Often abbreviated as [Ipc][].

[Ipc]: #indeclinable-particle
[indeclinable particle]: #indeclinable-particle

Is a
----

-   [word class][]


inflectional category
=====================
[inflectional category]: #inflectional-category
[inflectional class]: #inflectional-class
[inflectional categories]: #inflectional-category

A more detailed categorization of a [word class][].
Things that belong to the same inflection category have the same
affix set.

Examples
--------

-   NI-1
-   VTA-n
-   NDA-4w

> ⚠️  **A deprecated synonym exists** — This was formerly also called an
> *inflectional class*, but that term is now deprecated.

inflectional paradigm
======================

[paradigm]: #inflectional-paradigm

The collection of inflected [wordforms] belonging to a lemma. Informally known as the [conjugations].

## Part of

- **1** [lemma]

## Contains

- **1** or more [wordform]


general word class
=====================
[general word class]: #general-word-class

Superclass of [word class][]. Does not contain [inflectional categories][].

General word classes are are not detailed
enough to tell you how its members [inflect]. A [word class][], on the
other hand, tells you enough to be able to [inflect].

Consists of
-----------

-   **1 or more** [word classes][]

In Plains Cree
--------------

* Noun — contains the word classes: [NI], [NA], [NID], [NAD]
* Verb — contains the word classes: [VII], [VAI], [VTI], [VTA]
* Indeclinable particle


gloss
=====
[gloss]: #gloss

> Note: use [translation][] instead!

Sometimes a sloppy synonym for [translation][].
More specifically, a _gloss_ is a one-to-one
mapping between one language and another, often accompanied by relevant
[tags][tag] for [morphosyntactic features][]. Glosses are more
specific and less "fluent" than a [translation][].


head
====
[head]: #head
[heads]: #head

The highest level structure of a [dictionary][].
Each head is listed alphabetically (with derivations (phrases on the
[wordform][]) coming after the 'root' listing).

inflected form
==============
[inflect]: #inflect
[inflected form]: #inflected-form
[inflected forms]: #inflected-form

???

lacuna
======

"Gaps" in a [paradigm]. Any form that does not exist in a paradigm. For
example, the English word “pants”:

|   | Singular | Plural |
|:-:|:--------:|:------:|
|   |     —    | pants  |

[lacuna]: #lacuna
[lacunae]: #lacuna

Pants doesn't have a singular form! There's “pant leg”, but no “\*pant”
This is a **lacuna**: a gap in the paradigm, where you would otherwise
expect a valid form.


lemma
=====
[lemma]: #lemma
[lemmas]: #lemma
[lemmata]: #lemma
[base form]: #lemma
[baseform]: #lemma

The _base form_ of a [word form]; this is a form chosen to depict the basic
representation of the paradigm. Often the least structurally and
semantically marked form.  Unlike a [stem] or [root], a lemma is always
a valid [word form].

In a dictionary, the definitions of a lemma implicitly provide definitions for
the inflected forms of the lemma.

> ⚠️ **FIXME** — in itwêwina, we have been associating additional definitions
> with non-lemma wordforms. This is somewhat at odds with typical linguistic
> usage, where a lemma is the canonical form of a lexeme. Then, providing a
> definition for a wordform implies that the wordform is its own lexeme.

If a term is defined in a dictionary, its [head] will be the lemma.
e.g., you might not find a definition for "smartphones" in a dictionary of
contemporary English; instead, you'll find a definition for
"smartphone" (the lemma), and "smartphones" is one of its [inflected
forms]. However, non-lemma wordforms may also be [heads] in a dictionary,
depending on context.

### Part of

* **1** or more [word form]
* **1** [head]

lexeme
=====

A related set of wordforms.

Other sources may also call this a lexical entry or lexical item.

meaning
========
[meaning]: #meaning

???


morpheme
========
[morpheme]: #morpheme

An indivisible part of language with meaning; A morpheme cannot be
broken down into any subsequent parts, without changing its meaning.


morphosyntactic feature
=======================
[morphosyntactic feature]: #morphosyntactic-feature
[morphosyntactic features]: #morphosyntactic-feature

???

multicharacter symbol
=====================
[multicharacter symbol]: #multicharacter-symbol

In LEXC, a symbol in the FST's alphabet that is realized in text form
as multiple Unicode characters. These are used for tags, e.g., `+V`,
`+TA`, `+Err/Orth`; and special symbols used in phonological rules,
e.g., the `t2` in `nit2<nipa>n`.

Note to FST implementors: since tags are **always** multicharacter
symbols, if the FST output has all the symbols separated, then
there is no need to parse the analysis to find tags.

For example, "nêpât" is transduced to the following ten symbols
(separated by `|`):

    IC+ | n | i | p | â | w | +V | +AI | +Cnj | +3Sg


normatize
=========
[normatize]: #normatize

Write things according to the orthographical _norm_. A norm is
implicitly and unconsciously decided by a community of writers. To
normalize the spelling of something is to make it match the spelling
expected by a community. A language may have many norms.

See also: [standardize][]

- e.g., the normative form of "alot" is "a lot"
- e.g., the normative form of "icecream" is "ice cream"
- e.g., the normative form of "atchakosuk" is "acâhkosak"

orthographical representation
=============================
[orthographical representation]: #orthographical-representation
[orthographical representations]: #orthographical-representation

???

paradigm layout
===============
[paradigm layout]: #paradigm-layout

A formal specification that describes how to arrange (in a table)
the inflections or derived wordforms of any lexemes belonging to
a particular [word class]; or, how to arrange related wordforms in
a table.

Subtypes:
<dl>
<dt>dynamic paradigm layout</dt>
<dd>paradigm layout that has placeholders for the lemma or other
morphosyntactic information that may be replaced when generating
a rendered paradigm. These are the types of paradigm layouts used when
describing an entire word class.</dd>
<dt>static paradigm layout</dt>
<dd>paradigm layout in which all forms are explicitly
specified; there are no placeholders</dd>
</dl>


part of speech
==============
[part of speech]: #part-of-speech

> ⚠️  **Deprecated** — use [word class][] instead.

The grammatical category to which a [term][] belongs.
Different parts of speech have different functions in a
clause.

Part of
-------

-   **1** or more [word class][]
-   **1** [term][]


phrase
======
[phrase]: #phrase

Multiple [word forms][] that, together, have one [meaning][].
A [dictionary entry][] may use a phrase as a [head][].

Is composed of
--------------

-   **2 or more** [word forms][]

Can be a
--------

-   **1** [head][]


root
====
[root]: #root

The smallest form of a term (a morpheme) from which all [inflected forms][] are based off
of. The root might not be a valid [wordform].

For example, in English, _childr-_ is the root of _child_ and
_children_.

### In Plains Cree

 - _\*atimw-_ is the root of the lemma
   [atim](https://itwewina.dev/?q=atim), however, it is not a valid
   wordform on its own. It can be inflected to create _atim_ and
   _atimwak_.
 * _mow-_ is the root of the lemma [mowêw](https://itwewina.dev/?q=mowêw),
   and it also happens to be a valid inflected form of mowêw (an
   imperative form)


source language
===============
[source language]: #source-language

In a unidirectional bilingual dictionary, the language of the [head][]
words.

Example: in *Cree: Words*, which gives a list of Cree [head][] words
with all [definitions][] being English [translations][], the source
language is Cree.

See also: [target language][].


standardize
===========
[standardize]: #standardize

Write things according to the orthographical _standard_. A standard is
explicitly and consciously decided by an individual or body to be
adopted by a greater community. A language may have many standards, or
it might have no standard orthography. When there is one widely-adopted
standard, then it is also the norm: then "standardize" and "normative"
are synonymous.

See also: [normatize][]


tag
===
[tag]: #translation

A [multicharacter symbol] that represents a linguistic feature.


In Plains Cree
--------------

In the Plains Cree FST, these tags either end with a `+` for prefixes (e.g.,
`PV/e+`, or start with `+` sign for everything else (e.g., `+N`, `+TA`,
`+V`).

 - General word class: `+V`, `+N`, `+Ipc`, `+Prop`
 - Word class `+TA`, `+TI`, `+VI`, `+I`, `+A`
 - Whether a noun is dependent: `+D`
 - Tense: `+Prs`, `+Fut`, `+Prt` (really, denotes which tense preverb exists)
 - Order: `+Ind`, `+Cnj`
 - Subject: `+1Sg`, `+3Pl`, `+4Sg/Pl`, `+5Sg/Pl`
 - Object: `+1SgO`, `+3PlO`, `+4Sg/PlO`
 - The possessor of a noun: `+Px1Sg`, `+Px2Sg`, `+Px4Sg`
 - Preverbs: `PV/e+`, `PV/kaa+`
 - Reduplcation: `RdplW+`, `RdplS+`
 - and many more!

See this document for more info: https://giellalt.uit.no/lang/crk/crk.html


target language
===============
[target language]: #target-language

In a unidirectional bilingual dictionary, the language of the definitions.

Example: in *Cree: Words*, which gives a list of Cree [head][] words
with all [definitions][] being English [translations][], the target
language is English.

See also: [source language][].


translation
===========

[translation]: #translation
[translations]: #translation

A [definition][] written in a different language than the [head][]
it is defining.


user query
==========
[user query]: #user-query


_also **query**, **search string**_.

How the user writes their _search intent_, as a series of Unicode code
points. This might be a messy, misspelled, strangely written string.
It is the job of the intelligent dictionary to take this wild thing
and make sense of it, returning results that satisfy the user's search
intent.


word class
==========
[word class]: #word-class
[word classes]: #word-class

Category of a set of terms that [inflect][] in a similar way. Members of the
same word class behave morphologically in a similar way to each other.

Contains
--------

-   **1 or more** [inflectional categories][].

in Plains Cree
--------------

[NAD]: #NAD
[NA]: #NA
[NA]: #NA
[NID]: #NID
[NI]: #NI
[VAI]: #VAI
[VII]: #VII
[VTA]: #VTA
[VTI]: #VTI

These are the word classes in Plains Cree:
<a id="#NA"></a><a id="#NA"></a><a id="#NAD"></a><a id="#NI"></a><a id="#NID"></a><a id="#VAI"></a><a id="#VII"></a><a id="#VTA"></a><a id="#VTI"></a>

-   NA: 🧑🏽 — **a**nimate **n**oun
-   NI: 📘 — **i**nanimate **n**oun
-   NAD: 👤🧑🏽 — **d**ependent **a**nimate **n**oun
-   NID: 👤📘 — **d**ependent **i**nanimate **n**oun
-   VII: 📘➡️ — **i**ntransitive **i**nanimate **v**erb
-   VAI: 🧑🏽➡️ — **i**ntransitive **a**nimate **v**erb
-   VTI: 🧑🏽➡️📘— **t**ransitive **i**nanimate **v**erb
-   VTA: 🧑🏽➡️🧑🏽— **t**ransitive **i**nanimate **v**erb
-   [Ipc][]

More specific categorizations inside a word class are [inflectional
categories][] such as NI-1.

> ⚠️  **A deprecated synonym exists** — This was formerly also called a
> *specific word class*, but that term is now deprecated.

wordform
========
[wordform]: #wordform
[wordforms]: #wordform
[word form]: #wordform
[word forms]: #wordform

In linguistics, the different ways that a word can exist in a language.
(Not to be confused with [lemma] – which is its own special type of
wordform). A wordform _must_ be able to exist by itself. Contrast this
to [morpheme][] and [phrase][].


stem
====
[stem]: #stem

In linguistics, please use the term [root][] instead.

In natural language processing and information retrieval, the stem is a
potentially garbled form of the input term that aids in indexing a large
number of related terms. Typically this involves using naïve heuristics to
remove both inflectional and derivational affixes from the input term. The
stem does _not_ have to be linguistically meaningful, and the stem is often
not a valid [wordform].

For example, "connection" can be _stemmed_ to "connect" using the [Porter
stemming algorithm].

Naïve stemming heuristics can be replaced with a linguistic analyzer
that is able to return the [lemma][] of a term, however, this is not
available for every language, and may not be necessary to create
a satisfactory information retrieval system.

[Porter stemming algorithm]: https://tartarus.org/martin/PorterStemmer/def.txt

term
====
[term]: #term
[terms]: #term

???
