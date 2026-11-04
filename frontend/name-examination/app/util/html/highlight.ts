const escapeRegExp = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

export const highlightWord = (word: string, text: string, highlightCss: string) => {
  if (!word) return text
  const re = new RegExp(escapeRegExp(word), 'gi')
  return text.replace(re, (match: string) => `<span class="${highlightCss}">${match}</span>`)
}
