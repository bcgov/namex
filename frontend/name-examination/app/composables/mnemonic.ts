/**
 * Support for triggering an action when a mnemonic is triggered (Alt key + some letter)
 */
export function useMnemonic(letter: string, callback: () => void) {
  function handleKeydown(event: KeyboardEvent) {
    if (event.altKey && event.key === letter.toLowerCase()) {
      callback()
      event.preventDefault()
    }
  }

  onMounted(() => window.addEventListener('keydown', handleKeydown))
  onUnmounted(() => window.removeEventListener('keydown', handleKeydown))
}
