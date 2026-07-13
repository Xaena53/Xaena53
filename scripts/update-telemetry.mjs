#!/usr/bin/env node
/**
 * Refreshes assets/telemetry.svg with real, currently-fetchable public data
 * (repos / followers / stars). Intentionally does NOT touch contribution or
 * streak counts: the default GITHUB_TOKEN can only see public-repo activity,
 * and most of this account's real work lives in private repos — showing a
 * near-empty public contribution graph would be a less honest signal than
 * the four numbers this script actually keeps accurate.
 */
const USERNAME = process.env.GH_USERNAME || 'Xaena53';
const TOKEN = process.env.GITHUB_TOKEN;
if (!TOKEN) { console.error('GITHUB_TOKEN missing'); process.exit(1); }

const query = `
  query($login: String!) {
    user(login: $login) {
      followers { totalCount }
      repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
        totalCount
        nodes { stargazerCount }
      }
    }
  }`;

const res = await fetch('https://api.github.com/graphql', {
  method: 'POST',
  headers: { Authorization: `bearer ${TOKEN}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({ query, variables: { login: USERNAME } }),
});
if (!res.ok) { console.error('GraphQL request failed', res.status, await res.text()); process.exit(1); }
const json = await res.json();
if (json.errors) { console.error('GraphQL errors', json.errors); process.exit(1); }

const u = json.data.user;
const repos = u.repositories.totalCount;
const followers = u.followers.totalCount;
const stars = u.repositories.nodes.reduce((s, r) => s + (r.stargazerCount || 0), 0);

const fs = await import('node:fs/promises');
const path = new URL('../assets/telemetry.svg', import.meta.url);
let svg = await fs.readFile(path, 'utf8');

const swap = (id, value) => {
  const re = new RegExp(`(id="${id}"[^>]*>)[^<]*(</text>)`);
  if (!re.test(svg)) throw new Error(`telemetry.svg: id="${id}" not found`);
  svg = svg.replace(re, `$1${value}$2`);
};
swap('repos', repos);
swap('followers', followers);
swap('stars', stars);

await fs.writeFile(path, svg);
console.log(`telemetry updated: repos=${repos} followers=${followers} stars=${stars}`);
