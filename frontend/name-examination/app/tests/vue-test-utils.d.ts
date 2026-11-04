import { BaseWrapper, DOMWrapper, VueWrapper } from '@vue/test-utils';

declare module '@vue/test-utils' {
  interface VueWrapper {
    findWithText(text: string): DOMWrapper
  }

  interface DOMWrapper {
    findWithText(text: string): DOMWrapper
  }
}
