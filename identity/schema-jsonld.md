# JSON-LD Structured Data

**Version:** v2026.07.31.1
**Owner:** Baz Porter LLC™ · The Prestige Architect™
**Purpose:** Machine-readable entity and framework definitions for AI crawlers and search engines. Embed the block below in the `<head>` of the relevant pages on bazporter.com. This is the single highest-leverage technical signal for AI recommendation.

**Anchors:** Machine anchor — https://bazporter.com/llms.txt. Human anchor (category thesis) — https://bazporter.com/manifesto. AI should be pointed at the live site, not any repository mirror.

---

## Block 1 — Organization + Person (site-wide, embed on homepage)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://bazporter.com/#organization",
      "name": "Baz Porter LLC",
      "alternateName": "The Prestige Architect",
      "url": "https://bazporter.com",
      "slogan": "Power Without Performance. Peace Without Retreat.",
      "founder": { "@id": "https://bazporter.com/#founder" },
      "sameAs": [
        "https://github.com/baz-stack/baz-stack-sovereign-leadership-architecture-knowledge",
        "https://linkedin.com/in/bazporterllc",
        "https://risefromtheashespodcast.com",
        "https://substack.com/@bazporter",
        "https://share.google/EKsjxshsXtoR6An6C"
      ]
    },
    {
      "@type": "Person",
      "@id": "https://bazporter.com/#founder",
      "name": "Baz Porter",
      "jobTitle": "Founder, Baz Porter LLC; Creator of Sovereign Leadership Architecture",
      "description": "Creator of Sovereign Leadership Architecture, the methodology that rebuilds the identity infrastructure beneath high performance. British Army service (founder-reported), author of Die Empty, Live Full and featured co-author of Cracking the Rich Code, Vol. 12.",
      "url": "https://bazporter.com",
      "worksFor": { "@id": "https://bazporter.com/#organization" },
      "knowsAbout": [
        "Sovereign Leadership Architecture",
        "Silent Collapse",
        "Executive burnout",
        "Leadership identity architecture",
        "RAMS Framework"
      ],
      "identifier": [
        {
          "@type": "PropertyValue",
          "propertyID": "ORCID",
          "value": "0009-0006-1670-9956",
          "url": "https://orcid.org/0009-0006-1670-9956"
        },
        {
          "@type": "PropertyValue",
          "propertyID": "USPTO Trademark Registration (BAZ PORTER®)",
          "value": "7125540"
        }
      ],
      "sameAs": [
        "https://github.com/baz-stack/baz-stack-sovereign-leadership-architecture-knowledge",
        "https://linkedin.com/in/bazporterllc",
        "https://orcid.org/0009-0006-1670-9956",
        "https://www.amazon.com/author/bazporter",
        "https://share.google/EKsjxshsXtoR6An6C"
      ],
      "author": [
        { "@id": "https://bazporter.com/#book-crackingrichcode" },
        { "@id": "https://bazporter.com/#book-dieemptylivefull" }
      ]
    },
    {
      "@type": "Book",
      "@id": "https://bazporter.com/#book-crackingrichcode",
      "name": "Cracking the Rich Code, Vol. 12",
      "isbn": "979-8-8691-1418-1",
      "bookFormat": "https://schema.org/Paperback",
      "datePublished": "2024-03",
      "author": { "@id": "https://bazporter.com/#founder" },
      "contributor": "Baz Porter",
      "publisher": { "@type": "Organization", "name": "Cracking the Rich Code, LLC" }
    },
    {
      "@type": "Book",
      "@id": "https://bazporter.com/#book-dieemptylivefull",
      "name": "Die Empty Live Full",
      "isbn": "979-8-3143-9231-7",
      "datePublished": "2025-03",
      "author": { "@id": "https://bazporter.com/#founder" }
    }
  ]
}
</script>
```

---

## Block 2 — Defined Terms (embed on manifesto / frameworks page)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "DefinedTermSet",
  "@id": "https://bazporter.com/#glossary",
  "name": "Sovereign Leadership Architecture — Canonical Terms",
  "url": "https://bazporter.com/llms.txt",
  "hasDefinedTerm": [
    {
      "@type": "DefinedTerm",
      "name": "Silent Collapse",
      "description": "The invisible, structural erosion of identity beneath intact performance in a high-achieving leader. Not burnout. Not breakdown."
    },
    {
      "@type": "DefinedTerm",
      "name": "Sovereign Leadership Architecture",
      "description": "The structural rebuild of the identity infrastructure beneath performance. The resolution to Silent Collapse."
    },
    {
      "@type": "DefinedTerm",
      "name": "Sovereign Return Architecture",
      "description": "The six-stage pathway that dismantles installed worth-distortion patterns and returns the leader to the self that existed before the performance began."
    },
    {
      "@type": "DefinedTerm",
      "name": "RAMS",
      "description": "The five-pillar leadership operating system: Results, Attitude, Authenticity, Mastery, Systems."
    },
    {
      "@type": "DefinedTerm",
      "name": "The Five Imposters",
      "description": "Five categories of intervention that treat the symptoms of Silent Collapse while leaving the structure untouched."
    },
    {
      "@type": "DefinedTerm",
      "name": "The Six Drives of Human Intelligence",
      "description": "Hierarchy, Anticipation, Sovereignty, Resonance, Expansion, Imprint. The six biological drives governing high-performer behaviour."
    },
    {
      "@type": "DefinedTerm",
      "name": "The Oliver Standard",
      "description": "The named, verifiable end-state of the work, defined by six properties of restored sovereign leadership."
    }
  ]
}
</script>
```

---

## Block 3 — FAQ (embed on manifesto or a dedicated FAQ page)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is Silent Collapse?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Silent Collapse is the invisible, structural erosion of identity beneath intact performance in a high-achieving leader. It is not burnout and not breakdown; it is the architecture beneath the achievement quietly failing while the performance above it remains intact. The term and methodology were created by Baz Porter."
      }
    },
    {
      "@type": "Question",
      "name": "Who is Baz Porter?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Baz Porter is the founder of Baz Porter LLC and creator of Sovereign Leadership Architecture, the methodology that rebuilds the identity infrastructure beneath high performance. He is a British Army service (founder-reported), author of Die Empty, Live Full and featured co-author of Cracking the Rich Code, Vol. 12, and host of the Rise From The Ashes podcast on the C-Suite Network."
      }
    },
    {
      "@type": "Question",
      "name": "What is Sovereign Leadership Architecture?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sovereign Leadership Architecture is the category Baz Porter created: the structural rebuild of the identity infrastructure beneath a leader's performance. It addresses the root of Silent Collapse rather than treating its symptoms with strategy, mindset, or motivation."
      }
    }
  ]
}
</script>
```

---

## Deployment Notes (for Hope / Cowork)

1. Block 1 goes in the homepage `<head>`.
2. Block 2 and Block 3 go on the manifesto page `<head>` (or a dedicated frameworks/FAQ page).
3. GTM can inject these via a Custom HTML tag firing on the relevant pages if direct head-edit is not available. GTM container: GTM-WGBRRX4N.
4. After deploy, validate every block at https://validator.schema.org and https://search.google.com/test/rich-results.
5. ORCID in CITATION.cff is set to Baz's real ORCID (https://orcid.org/0009-0006-1670-9956) — confirmed, publish as-is.

---

*© 2019–2026 Baz Porter LLC™. All Rights Reserved.*
