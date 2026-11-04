/**
 * Represents an action.
 */
import { faker } from '@faker-js/faker'
import { v4 as uuidv4 } from 'uuid'
import Utilities from './Utilities'
const util = new Utilities()

const regex = new RegExp('@[0-9]{8}')

class Action {}

export default Action
