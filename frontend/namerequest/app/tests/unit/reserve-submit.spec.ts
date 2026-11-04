// import ReserveSubmit from '@/components/new-request/submit-request/reserve-submit.vue'
import { createLocalVue } from '@vue/test-utils'
// import { mount } from '@vue/test-utils'
import Vuetify from 'vuetify'
// import sinon from 'sinon'

const localVue = createLocalVue()
// const vuetify = new Vuetify()

localVue.use(Vuetify)

/* commented out lines and blocks of tests were correct and passing before it was decided not to allow auto
   analyze approvals and conditional approvals */

// async function provideWrapper (setup) {
//   const wrapper = mount(ReserveSubmit, {
//     localVue,
//     vuetify,
//     propsData: {
//       setup
//     }

//   })
//   await wrapper.vm.$nextTick()
//   return wrapper
// }

// const sandbox = sinon.createSandbox()

describe('ReserveSubmit component', () => {
  it('is an empty test', () => {})
  // describe('Case: it handles the NORMAL route (!setup) properly', () => {
  //   sandbox.spy(newReqModule, 'postNameRequest')
  //   let wrapper: any

  //   beforeEach(async (done) => {
  //     wrapper = await provideWrapper('')
  //     done()
  //   })
  //   afterAll(() => {
  //     newReqModule.mutateLocation('BC')
  //   })
  //   afterEach(() => {
  //     sandbox.reset()
  //     wrapper.destroy()
  //   })
  //   test('The button is labelled "Continue"', async () => {
  //     await newReqModule.mutateLocation('BC')
  //     wrapper.vm.$nextTick()
  //     expect(wrapper.text()).toBe('Continue')
  //     // expect(wrapper.text()).toBe('Reserve and Continue')
  //   })
  //   describe('If location === "BC", it acts as a RESERVED name', () => {
  //     test('postNameRequest("reserved") is called with correct argument', async () => {
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       // expect(newReqModule.postNameRequest.calledOnce).toBeTruthy()
  //       // expect(newReqModule.postNameRequest.getCall(0).args[0] === 'reserved').toBeTruthy()
  //       expect(newReqModule.postNameRequest.calledOnce).toBeFalsy()
  //     })
  //     /*
  //     test('submissionType is set to "normal"', async () => {
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionType === 'normal').toBeTruthy()
  //     })
  //     test('The UI displays Applicant-Info-1', async () => {
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionTabNumber === 2).toBeTruthy()
  //     }) */
  //   })
  //   describe('If location !== "BC", it sends to examination', () => {
  //     test('postNameRequest is not called', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.postNameRequest.calledOnce).toBeFalsy()
  //     })
  //     test('submissionType is set to "examination"', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionType === 'examination').toBeTruthy()
  //     })
  //     test('The UI displays NamesCapture', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionTabNumber === 1).toBeTruthy()
  //     })
  //   })
  // })

  // describe('Case: it handles the CONDITIONAL route (setup === "consent") properly', () => {
  //   let wrapper: any
  //   beforeEach(async (done) => {
  //     wrapper = await provideWrapper('consent')
  //     done()
  //   })
  //   afterEach(() => {
  //     sandbox.reset()
  //     wrapper.destroy()
  //   })
  //   test('The button is labelled "Continue"', () => {
  //     expect(wrapper.text()).toContain('Continue')
  //     /* Whenever auto-approvals are turned back on again, replace line 108 with the following:
  //        expect(wrapper.text()).toContain('Conditionally Reserve') */
  //   })
  //   /* Whenever auto-approvals are turned back on again, these tests should pass once again, can remove comments

  //   describe('If location === "BC", it acts as a RESERVED-CONDITION name', () => {
  //     test('postNameRequest("conditional") is called with correct argument', async () => {
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.postNameRequest.calledOnce).toBeTruthy()
  //       expect(newReqModule.postNameRequest.getCall(0).args[0] === 'conditional').toBeTruthy()
  //     })
  //     test('submissionType is set to "consent"', async () => {
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionType === 'consent').toBeTruthy()
  //     })
  //     test('The UI displays Applicant-Info-1', async () => {
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionTabNumber === 2).toBeTruthy()
  //     })
  //   }) */
  //   test('The UI displays names-capture', async () => {
  //     wrapper.vm.handleSubmit()
  //     await wrapper.vm.$nextTick()
  //     // 1 === names-capture tab
  //     expect(newReqModule.submissionTabNumber).toEqual(1)
  //   })
  //   describe('If location !== "BC", it sends to examination', () => {
  //     test('postNameRequest is not called', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.postNameRequest.calledOnce).toBeFalsy()
  //     })
  //     test('submissionType is set to "examination"', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionType === 'examination').toBeTruthy()
  //     })
  //     test('The UI displays NamesCapture', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionTabNumber === 1).toBeTruthy()
  //     })
  //   })
  // })

  // describe('Case: it handles the EXAMINATION route (setup === "examine") properly', () => {
  //   let wrapper: any
  //   beforeEach(async (done) => {
  //     wrapper = await provideWrapper('examine')
  //     done()
  //   })
  //   afterEach(() => {
  //     sandbox.reset()
  //     wrapper.destroy()
  //   })
  //   test('The button is labelled "Continue"', () => {
  //     expect(wrapper.text()).toBe('Continue')
  //   })
  //   describe('If location === "BC", it sends to examination', () => {
  //     newReqModule.mutateLocation('BC')
  //     test('postNameRequest is not called', async () => {
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.postNameRequest.calledOnce).toBeFalsy()
  //     })
  //     test('submissionType is set to "examination"', async () => {
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionType === 'examination').toBeTruthy()
  //     })
  //     test('The UI displays NamesCapture', async () => {
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionTabNumber === 1).toBeTruthy()
  //     })
  //   })
  //   describe('If location !== "BC", it sends to examination', () => {
  //     test('postNameRequest is not called', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.postNameRequest.calledOnce).toBeFalsy()
  //     })
  //     test('submissionType is set to "examination"', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionType === 'examination').toBeTruthy()
  //     })
  //     test('The UI displays NamesCapture', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionTabNumber === 1).toBeTruthy()
  //     })
  //   })
  // })

  // describe('Case: it handles the ASSUMED route (setup === "assumed") properly', () => {
  //   let wrapper: any
  //   newReqModule.mutateName('Original Assumed Name Ltd.')

  //   beforeEach(async (done) => {
  //     wrapper = await provideWrapper('assumed')
  //     done()
  //   })
  //   afterAll(() => {
  //     sandbox.restore()
  //   })
  //   afterEach(() => {
  //     sandbox.reset()
  //     wrapper.destroy()
  //   })
  //   test('The button is labelled "Continue"', () => {
  //     expect(wrapper.text()).toBe('Continue')
  //   })

  //   for (let code of ['XCR', 'RLC', 'XUL']) {
  //     let createTest = async () => {
  //       describe(`If the entity_type_cd is ${code}`, () => {
  //         newReqModule.mutateLocation('CA')
  //         newReqModule.mutateEntityType(`${code}`)
  //         test('postNameRequest is not called', async () => {
  //           wrapper.vm.handleSubmit()
  //           await wrapper.vm.$nextTick()
  //           expect(newReqModule.postNameRequest.calledOnce).toBeFalsy()
  //           newReqModule.mutateRequestAction('NEW')
  //         })
  //         test(`assumedNameOriginal is set to newReqModule.name`, async () => {
  //           wrapper.vm.handleSubmit()
  //           await wrapper.vm.$nextTick()
  //           expect(newReqModule.assumedNameOriginal === newReqModule.name).toBeTruthy()
  //         })
  //         test('submissionType is set to "examination"', async () => {
  //           newReqModule.mutateLocation('CA')
  //           wrapper.vm.handleSubmit()
  //           await wrapper.vm.$nextTick()
  //           expect(newReqModule.submissionType === 'examination').toBeTruthy()
  //         })
  //         test('The UI displays NamesCapture', async () => {
  //           newReqModule.mutateLocation('CA')
  //           wrapper.vm.handleSubmit()
  //           await wrapper.vm.$nextTick()
  //           expect(newReqModule.submissionTabNumber === 1).toBeTruthy()
  //         })
  //       })
  //     }
  //     createTest()
  //   }
  //   describe('If the entity_type_cd is not one that can be ASSUMED', () => {
  //     newReqModule.mutateLocation('CA')
  //     newReqModule.mutateName('Another Test Name Ltd.')
  //     test('assumedNameOriginal is set to newRequestModule.name', async () => {
  //       expect(newReqModule.assumedNameOriginal === newReqModule.name).toBeTruthy()
  //     })
  //     test('submissionType is set to "examination"', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionType === 'examination').toBeTruthy()
  //     })
  //     test('The UI displays NamesCapture', async () => {
  //       newReqModule.mutateLocation('CA')
  //       wrapper.vm.handleSubmit()
  //       await wrapper.vm.$nextTick()
  //       expect(newReqModule.submissionTabNumber === 1).toBeTruthy()
  //     })
  //   })
  // })
})
