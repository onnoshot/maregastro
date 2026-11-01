// Telefon numaralarinin tek bicimi: E.164 (+905321234567).
// Eski kayitlar yazilmadan okunurken ayni kuralla cevrilir; cevrilemeyen numara silinmez,
// phoneOk:false ile panele isaretlenir. Musterinin talebi telefon yuzunden asla reddedilmez.
import { parsePhoneNumberFromString as parse } from 'libphonenumber-js/max';

const toLatinDigits = (s) => s
  .replace(/[٠-٩]/g, (d) => d.charCodeAt(0) - 0x0660)
  .replace(/[۰-۹]/g, (d) => d.charCodeAt(0) - 0x06f0);

function bestMatch(raw) {
  const s = toLatinDigits(String(raw || '')).trim();
  const digits = s.replace(/\D/g, '');
  if (!digits) return null;
  const international = /^(\+|00)/.test(s);
  const asIntl = () => parse('+' + digits.replace(/^00/, ''));
  const asTr = () => parse(s, 'TR');
  const tries = international ? [asIntl()] : [asTr(), asIntl()];
  return tries.find((n) => n && n.isValid()) || tries.find((n) => n && n.isPossible()) || null;
}

export function normalizePhone(raw) {
  const n = bestMatch(raw);
  if (!n) return { phone: String(raw || '').trim(), phoneDisplay: String(raw || '').trim(), phoneCountry: '', phoneOk: false };
  return { phone: n.number, phoneDisplay: n.formatInternational(), phoneCountry: n.country || '', phoneOk: true };
}

// Panele giden kayit: telefon her zaman tek bicimde, ek alanlar yalnizca yanitta.
export function withPhone(rec) {
  return { ...rec, ...normalizePhone(rec.phone) };
}
