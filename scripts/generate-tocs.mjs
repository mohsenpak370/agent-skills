#!/usr/bin/env node
// Adds or refreshes a "## Contents" table of contents in long skill Markdown
// files so agents previewing only the top of a file can see its full scope.
//
// Usage: node scripts/generate-tocs.mjs [--check] [--min-lines N] [paths...]
// Defaults to skills/ and references/. Generated blocks are wrapped in
// <!-- toc --> markers and rewritten on each run; files that already have an
// unmarked contents section are left alone.

import { readdir, readFile, writeFile, stat } from "node:fs/promises";
import { join } from "node:path";

const args = process.argv.slice(2);
const check = args.includes("--check");
const minIdx = args.indexOf("--min-lines");
const minLines = minIdx >= 0 ? Number(args[minIdx + 1]) : 100;
const roots = args.filter((a, i) => !a.startsWith("--") && (minIdx < 0 || i !== minIdx + 1));
if (roots.length === 0) roots.push("skills", "references");

const MAX_ENTRIES = 40;
const MIN_ENTRIES = 3;
const START = "<!-- toc -->";
const END = "<!-- /toc -->";
const UNMARKED_TOC = /^#{2,3}\s+(table of contents|contents|toc)\s*$/im;

async function* markdownFiles(path) {
  const info = await stat(path);
  if (info.isFile()) {
    if (path.endsWith(".md")) yield path;
    return;
  }
  for (const entry of await readdir(path, { withFileTypes: true })) {
    if (entry.name === "node_modules" || entry.name.startsWith(".")) continue;
    yield* markdownFiles(join(path, entry.name));
  }
}

function headingText(raw) {
  return raw
    .replace(/\s+#+\s*$/, "")
    .replace(/!?\[([^\]]*)\]\([^)]*\)/g, "$1")
    .trim();
}

function slugify(text, seen) {
  const base = text
    .toLowerCase()
    .replace(/<[^>]+>/g, "")
    .replace(/[^\p{L}\p{N}\s_-]/gu, "")
    .replace(/ /g, "-");
  const count = seen.get(base) ?? 0;
  seen.set(base, count + 1);
  return count === 0 ? base : `${base}-${count}`;
}

function parse(lines) {
  let i = 0;
  if (lines[0] === "---") {
    const close = lines.indexOf("---", 1);
    if (close > 0) i = close + 1;
  }
  const bodyStart = i;
  const headings = [];
  let fence = null;
  for (; i < lines.length; i++) {
    const line = lines[i];
    const fenceMatch = line.match(/^\s*(```+|~~~+)/);
    if (fenceMatch) {
      const marker = fenceMatch[1];
      if (!fence) fence = marker;
      else if (marker[0] === fence[0] && marker.length >= fence.length) fence = null;
      continue;
    }
    if (fence) continue;
    const m = line.match(/^(#{1,6})\s+(.+)$/);
    if (m) headings.push({ level: m[1].length, text: headingText(m[2]), line: i });
  }
  return { bodyStart, headings };
}

function buildToc(headings) {
  const seen = new Map();
  const entries = headings.map((h) => ({ ...h, slug: slugify(h.text, seen) }));
  const h2 = entries.filter((h) => h.level === 2);
  let picked = entries.filter((h) => h.level === 2 || h.level === 3);
  if (picked.length > MAX_ENTRIES) picked = h2;
  if (picked.length < MIN_ENTRIES) return null;
  const top = Math.min(...picked.map((h) => h.level));
  return picked.map((h) => `${"  ".repeat(h.level - top)}- [${h.text}](#${h.slug})`);
}

function stripBlock(lines) {
  const s = lines.indexOf(START);
  const e = lines.indexOf(END);
  if (s < 0 || e < s) return lines;
  let end = e + 1;
  while (lines[end] === "") end++;
  return [...lines.slice(0, s), ...lines.slice(end)];
}

let changed = 0;
const skipped = [];
for (const root of roots) {
  for await (const file of markdownFiles(root)) {
    const original = await readFile(file, "utf8");
    const lines = stripBlock(original.split("\n"));
    if (lines.length <= minLines) continue;
    if (UNMARKED_TOC.test(lines.join("\n"))) continue;

    const { bodyStart, headings } = parse(lines);
    const h1 = headings.find((h) => h.level === 1 && h.line - bodyStart < 15);
    const toc = buildToc(headings.filter((h) => !h1 || h.line > h1.line));
    if (!toc) {
      skipped.push(file);
      continue;
    }

    let at = h1 ? h1.line + 1 : bodyStart;
    while (lines[at] === "") at++;
    const block = [START, "## Contents", "", ...toc, END, ""];
    const before = lines.slice(0, at);
    if (before.length && before[before.length - 1] !== "") before.push("");
    const next = [...before, ...block, ...lines.slice(at)].join("\n");

    if (next !== original) {
      changed++;
      if (check) console.log(`outdated: ${file}`);
      else await writeFile(file, next);
    }
  }
}

if (skipped.length) {
  console.log(`skipped (fewer than ${MIN_ENTRIES} usable headings): ${skipped.length}`);
  for (const f of skipped) console.log(`  ${f}`);
}
console.log(`${check ? "outdated" : "updated"}: ${changed}`);
if (check && changed) process.exit(1);
