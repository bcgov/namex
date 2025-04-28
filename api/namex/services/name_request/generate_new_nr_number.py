import random

from flask import current_app

from namex.models import NRNumberExclude, NRNumberLifespan, Request


def set_nr_num_lifespan(nr_num, span):
    """Set the lifespan of a number by deleting old entries and inserting the new one."""
    NRNumberLifespan.delete_old_entries(span)
    if NRNumberLifespan.check_nr_num_lifespan(nr_num):
        return False
    NRNumberLifespan.insert_nr_num(nr_num)
    return True


def check_nr_num_exists(nr_num):
    """Check if a number exists in the NRNumber table."""
    return bool(Request.find_by_nr(nr_num))


def check_nr_num_exclude(nr_num):
    """Check if a number exists in the NRNumExclude table."""
    return NRNumberExclude.check_nr_num_exclude(nr_num)


class NRNumberService:
    """
    Service class for handling operations related to NR numbers.

    This class provides methods for generating new NR numbers,
    ensuring they are unique and valid within a specified lifespan.
    """

    @classmethod
    def get_new_nr_num(cls):
        """
        Generate a new NR number that is unique and within the specified lifespan.

        Returns:
            str: A new unique NR number.
        """
        try:
            floor = 1  # assumed there is no NR 0000000
            ceiling = 9999999
            attempts = 100000000
            count = 0

            span = current_app.config.get('NR_NUM_LIFESPAN')

            while count < attempts:
                random_num = random.randint(floor, ceiling)  # noqa: S311
                nr_num = f'NR {str(random_num).zfill(7)}'
                count += 1

                if not set_nr_num_lifespan(nr_num, span):
                    continue

                if check_nr_num_exists(nr_num):
                    continue

                if check_nr_num_exclude(nr_num):
                    continue

                return nr_num

            raise Exception(f'Unable to generate random number from range {floor} to {ceiling} after {count} attempts.')
        except Exception as e:
            current_app.logger.error(f'Exception in get_new_nr_num; {str(e)}')
            raise
