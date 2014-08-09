Parsing logic 1
---------------

Most simple approach:

- Don't try anything even remotely smart
- Just detect word entry boundaries correctly,
    and render the paragraphs (separated by \n\n)
    as dt-less dd elements.


Parsing notes
-------------

Start of entry:
    - `^[A-Z][A-Z0-9 ;'-.,]*`
    - As above, and interspersed with `; `
    
Example:

    MALAY; MALAYAN
    Ma*lay", Ma*lay"an, a.

In the index, all words should be lowercased,
and multi-entry words should be duplicated.

---

The lines following the entry seem to contain some kind of syllabication info.

Example:

    MALAY; MALAYAN
    Ma*lay", Ma*lay"an, a.

In markdown output, remember to replace '*' with '-'

Tricky example:

    MALEFICE
    Mal"e*fice, n. Etym: [L. maleficium: cf. F. maléfice. See
    Malefactor.]

Perhaps the markdown treatment can be applied to the part before the `:`

---

Lines starting with `Defn: ` mark a definition -> DEFINITION
    - If there are multiple for an entry, subscript them -> DEFINITION-1

Example:

    MALAY; MALAYAN
    Ma*lay", Ma*lay"an, a.
    
    Defn: Of or pertaining to the Malays or their country.
     -- n.
    
    Defn: The Malay language. Malay apple (Bot.), a myrtaceous tree
    (Eugenia Malaccensis) common in India; also, its applelike fruit.

---

Lines starting with `\d+. \(\w+\.\)` *and* followed by a definition,
    should be treated as section headers.
    
Example:

    MALE
    Male, a. Etym: [F. mâle, OF. masle, mascle, fr. L. masculus male,
    masculine, dim. of mas a male; possibly akin to E. man. Cf.
    Masculine, Marry, v. t.]
    
    ...
    
    2. (Bot.)
    
    Defn: Capable of producing fertilization, but not of bearing fruit; -
    - said of stamens and antheridia, and of the plants, or parts of
    plants, which bear them.

---

Lines starting with `\d+. ` should be treated as sections.
    
Example:

    MALE
    Male, a. Etym: [F. mâle, OF. masle, mascle, fr. L. masculus male,
    masculine, dim. of mas a male; possibly akin to E. man. Cf.
    Masculine, Marry, v. t.]
    
    1. Of or pertaining to the sex that begets or procreates young, or
    (in a wider sense) to the sex that produces spermatozoa, by which the
    ova are fertilized; not female; as, male organs.
        
---

Synonyms are written in this format:

    MALEDICTION
    Mal`e*dic"tion, n. Etym: [L. maledictio: cf. F. malédiction. See
    Maledicent.]
    
    Defn: A proclaiming of evil against some one; a cursing; imprecation;
    a curse or execration; -- opposed to benediction.
    No malediction falls from his tongue. Longfellow.
    
    Syn.
     -- Cursing; curse; execration; imprecation; denunciation; anathema.
     -- Malediction, Curse, Imprecation, Execration. Malediction is the
    most general term, denoting bitter reproach, or wishes and
    predictions of evil. Curse implies the desire or threat of evil,
    declared upon oath or in the most solemn manner. Imprecation is
    literally the praying down of evil upon a person. Execration is
    literally a putting under the ban of excommunication, a curse which
    excludes from the kingdom of God. In ordinary usage, the last three
    words describe profane swearing, execration being the strongest.

Adding cross references (when perfect match exists) would be ideal.
