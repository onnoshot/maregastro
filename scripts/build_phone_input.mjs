// phone-input.js icindeki ulke tablosunu libphonenumber-js verisinden yeniden uretir.
// Calistirma: node scripts/build_phone_input.mjs (kutuphane guncellenince)
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { getCountries, getCountryCallingCode, Metadata } from 'libphonenumber-js/max';

const metadata = createRequire(import.meta.url)('libphonenumber-js/metadata.max.json');
const SKIP = new Set(['AC', 'TA', 'XK', 'SJ', 'BQ', 'EH', 'AX', 'GG', 'IM', 'JE']);
const MAX_OVERRIDE = { RU: 10, KZ: 10, TR: 10 };
const MIN_OVERRIDE = { TR: 10 };
const m = new Metadata(metadata);
const rows = getCountries().filter((c) => !SKIP.has(c)).map((c) => {
  m.selectNumberingPlan(c);
  const lens = m.numberingPlan.possibleLengths();
  const min = MIN_OVERRIDE[c] || Math.max(6, Math.min(...lens));
  const max = MAX_OVERRIDE[c] || Math.max(...lens);
  return [c, getCountryCallingCode(c), m.numberingPlan.nationalPrefix() || '', min, max].join(',');
});
const file = new URL('../phone-input.js', import.meta.url);
const next = readFileSync(file, 'utf8').replace(/var DATA='[^']*';/, "var DATA='" + rows.join(';') + "';");
writeFileSync(file, next);
console.log(rows.length, 'ulke');
