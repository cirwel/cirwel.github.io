# Spec Basin Reflections

This note explains the hidden `#spec-basin` block in `index.html`. It is a map
for future orientation, not public page copy.

## What This Is

The basin is a working map of what the CIRWEL / UNITARES work is being pulled
toward. It is not a final specialization label. Each top-level angle is a
direction of pull; each term inside an angle is a candidate vocabulary item.

The visible "specializing in" line does not maintain its own word list. It reads
`#spec-basin.angles`, flattens every angle's terms, and cycles that union. That
is the no-drift invariant: terms live in one place.

The JSON has four important parts:

- `angles`: the single source of candidate terms.
- `contributors`: who authored which top-level angle clusters.
- `angle_by`: the provenance map; its keys should match `angles` exactly.
- `grounding`: evidence bindings for terms that make claims about deployed
  systems, datasets, code paths, metrics, or paper mechanisms.

Current shape: 14 angles, 85 flattened terms, 15 grounded terms. `opus` owns 12
angles; `codex` owns 2.

## My Reading

The center of gravity is runtime self-reading. The strongest thread is not
"AI consciousness" as a loose claim; it is infrastructure for systems that can
estimate, expose, and regulate their own operating state while they are acting.

The risky edge is language outrunning measurement. Terms like "selfhood",
"interiority", "ipseity", or "phenomenology" can become impressive fog if they
are not tied back to actual observables. That is why the telemetry / grounding
angle matters: it pulls the vocabulary back toward EISV readings, calibration
gaps, saturation margins, trajectory windows, basin flips, and code-backed
mechanisms.

The sociality angle matters because a governed fleet is not just a pile of
isolated agent interiors. Roles, handoffs, protocols, trust, review loops, and
shared situational fields shape what each agent can become. In that sense,
fleet-level selfhood is partly negotiated between agents.

The control-theory angles are useful because they ask concrete questions:
Can the state be observed? Can it be steered? Does it remain stable under
intervention? What separates measurement from control? Those questions keep the
work from collapsing into pure metaphor.

The quantum-measurement angle is the one to handle most carefully. I read it as
a lens for measurement, complementarity, superposition-like ambiguity, and
back-action. I would not treat it as a physical claim about agents being quantum
systems.

"Basin, not point" is the right discipline. The project is still finding the
language that fits it. The basin lets several candidate names stay alive until
data, implementation, publication feedback, and outside readers make one or more
attractors harden.

## How To Extend It

When adding a term or angle:

1. Add new terms only under `angles`.
2. If adding a new top-level angle, add a matching `angle_by` entry.
3. Update the contributor's `contributors.*.angles` list.
4. Add `grounding` when a term refers to measured behavior, a dataset, a code
   path, or a published mechanism.
5. Do not create a second public or hidden list of the same terms.

Quick validation:

```sh
node -e "const fs=require('fs'); const h=fs.readFileSync('index.html','utf8'); const m=h.match(/<script type=\"application\/json\" id=\"spec-basin\">([\s\S]*?)<\/script>/); const d=JSON.parse(m[1]); const a=Object.keys(d.angles); const b=Object.keys(d.angle_by); const missing=a.filter(k=>!d.angle_by[k]); const extra=b.filter(k=>!d.angles[k]); console.log({angles:a.length, terms:a.flatMap(k=>d.angles[k]).length, missing, extra}); process.exit(missing.length || extra.length ? 1 : 0);"
```

## When You Feel Lost

Read the basin as a map, not a mandate. For any phrase, ask:

- What is being observed?
- What is being controlled or regulated?
- What is measured, and what is still only metaphor?

The good terms should survive those questions. The weak ones should either get
grounding or stay visibly provisional.
